"""Test rows with correct dimension order."""

import asyncio
import json
import sys
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_rows_correct_order():
    config = load_config()
    client = PlanningClient(config)
    
    # Correct POV order: Account, CostCenter, Currency, Entity, Future1, Period, Region, Scenario, Version, Years
    base_pov = {
        "members": [
            ["410000"],        # 1. Account
            ["Total CostCenter"], # 2. CostCenter
            ["USD"],           # 3. Currency
            ["Total Entity"],  # 4. Entity
            ["No Future1"],    # 5. Future1
            ["Dec"],           # 6. Period
            ["Total Region"],  # 7. Region
            ["Actual"],        # 8. Scenario
            ["Working"],       # 9. Version
            ["FY25"]           # 10. Years
        ]
    }
    
    test_cases = [
        {
            "name": "Rows: Account only",
            "rows": [{"members": [["410000"]]}]
        },
        {
            "name": "Rows: Account + CostCenter",
            "rows": [{"members": [["410000"], ["Total CostCenter"]]}]
        },
        {
            "name": "Rows: Account + CostCenter + Region",
            "rows": [{"members": [["410000"], ["Total CostCenter"], ["Total Region"]]}]
        },
        {
            "name": "Rows: Account + Entity",
            "rows": [{"members": [["410000"], ["Total Entity"]]}]
        },
        {
            "name": "Rows: CostCenter + Region",
            "rows": [{"members": [["Total CostCenter"], ["Total Region"]]}]
        },
        {
            "name": "Rows: Account + Entity + CostCenter + Region",
            "rows": [{"members": [["410000"], ["Total Entity"], ["Total CostCenter"], ["Total Region"]]}]
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
                    if "detail" in details:
                        import re
                        detail_match = re.search(r'"detail":"([^"]+)"', details)
                        if detail_match:
                            error_detail = detail_match.group(1)
                            print(f"[ERROR] {error_detail[:200]}")
                            # Check if error changed
                            if "row" not in error_detail.lower():
                                print("  -> Different error! This might be progress!")
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
    asyncio.run(test_rows_correct_order())




