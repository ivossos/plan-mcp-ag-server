"""Test rows with explicit dimension names specified."""

import asyncio
import json
import sys
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_with_dim_names():
    config = load_config()
    client = PlanningClient(config)
    
    base_pov = {
        "members": [
            ["410000"],        # 1. Account
            ["Total Entity"],  # 2. Entity
            ["Actual"],        # 3. Scenario
            ["FY25"],          # 4. Years
            ["Dec"],           # 5. Period
            ["Working"],       # 6. Version
            ["USD"],           # 7. Currency
            ["No Future1"],    # 8. Future1
            ["Total CostCenter"], # 9. CostCenter
            ["Total Region"]   # 10. Region
        ]
    }
    
    test_cases = [
        {
            "name": "Rows: Account with dimension name",
            "rows": [{"dimension": "Account", "members": [["410000"]]}]
        },
        {
            "name": "Rows: Account + CostCenter with dimension names",
            "rows": [
                {"dimension": "Account", "members": [["410000"]]},
                {"dimension": "CostCenter", "members": [["Total CostCenter"]]}
            ]
        },
        {
            "name": "Rows: Account + CostCenter + Region with dimension names",
            "rows": [
                {"dimension": "Account", "members": [["410000"]]},
                {"dimension": "CostCenter", "members": [["Total CostCenter"]]},
                {"dimension": "Region", "members": [["Total Region"]]}
            ]
        },
        {
            "name": "Rows: Single object with multiple dimensions",
            "rows": [{
                "dimension": "Account",
                "members": [["410000"], ["Total CostCenter"], ["Total Region"]]
            }]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"Testing: {test_case['name']}")
        print('='*80)
        
        grid_definition = {
            "suppressMissingBlocks": True,
            "pov": base_pov,
            "columns": [{"members": [["Dec"]]}],
            "rows": test_case["rows"]
        }
        
        print(f"Rows: {json.dumps(test_case['rows'], indent=2)}")
        
        try:
            result = await client.export_data_slice("PlanApp", "FinPlan", grid_definition)
            print("[SUCCESS!]")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:800])
            await client.close()
            return result
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response'):
                try:
                    error_text = await e.response.aread()
                    details = error_text.decode('utf-8', errors='ignore')
                    if "dimension" in details.lower() and "not recognized" in details.lower():
                        print("[ERROR] Dimension field not recognized - this format is wrong")
                    elif "detail" in details:
                        import re
                        detail_match = re.search(r'"detail":"([^"]+)"', details)
                        if detail_match:
                            print(f"[ERROR] {detail_match.group(1)[:250]}")
                        else:
                            print(f"[ERROR] {details[:300]}")
                    else:
                        print(f"[ERROR] {details[:300]}")
                except Exception:
                    print(f"[ERROR] {error_msg[:300]}")
            else:
                print(f"[ERROR] {error_msg[:300]}")
    
    await client.close()
    return None

if __name__ == "__main__":
    asyncio.run(test_with_dim_names())




