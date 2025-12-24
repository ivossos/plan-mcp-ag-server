"""Test rows with all 10 dimensions matching POV."""

import asyncio
import json
import sys
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_all_10_in_rows():
    config = load_config()
    client = PlanningClient(config)
    
    # POV with 10 dimensions
    pov_members = [
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
    
    test_cases = [
        {
            "name": "Rows: All 10 dimensions (same as POV)",
            "rows": [{"members": pov_members}]
        },
        {
            "name": "Rows: Account + CostCenter + Region (3 user dims)",
            "rows": [{"members": [["410000"], ["Total CostCenter"], ["Total Region"]]}]
        },
        {
            "name": "Rows: Account + Entity + CostCenter + Region (4 dims)",
            "rows": [{"members": [["410000"], ["Total Entity"], ["Total CostCenter"], ["Total Region"]]}]
        },
        {
            "name": "Rows: Account + Version + CostCenter + Region",
            "rows": [{"members": [["410000"], ["Working"], ["Total CostCenter"], ["Total Region"]]}]
        },
        {
            "name": "Rows: Account + Currency + Future1 + CostCenter + Region",
            "rows": [{"members": [["410000"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]]}]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"Testing: {test_case['name']}")
        print('='*80)
        
        grid_definition = {
            "suppressMissingBlocks": True,
            "pov": {"members": pov_members},
            "columns": [{"members": [["Dec"]]}],
            "rows": test_case["rows"]
        }
        
        print(f"Rows structure: {json.dumps(test_case['rows'], indent=2)}")
        
        try:
            result = await client.export_data_slice("PlanApp", "FinPlan", grid_definition)
            print("[SUCCESS!]")
            print(f"Result keys: {list(result.keys())}")
            if result.get("rows"):
                rows = result["rows"]
                print(f"Rows returned: {len(rows)}")
                if rows and rows[0].get("data"):
                    print(f"Data: {rows[0]['data']}")
            print(f"\nFull result:\n{json.dumps(result, indent=2, ensure_ascii=False)[:800]}")
            await client.close()
            return result
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response'):
                try:
                    error_text = await e.response.aread()
                    details = error_text.decode('utf-8', errors='ignore')
                    if "detail" in details:
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
    asyncio.run(test_all_10_in_rows())




