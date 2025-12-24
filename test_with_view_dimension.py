"""Test if View dimension is needed - maybe 11 dimensions total."""

import asyncio
import json
import sys
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_with_view():
    config = load_config()
    client = PlanningClient(config)
    
    # Try with View dimension added (11 dimensions total)
    # Order: Account, Entity, Scenario, Years, Period, View, Version, Currency, Future1, CostCenter, Region
    test_cases = [
        {
            "name": "11 dims: Account, Entity, Scenario, Years, Period, View, Version, Currency, Future1, CostCenter, Region",
            "pov": {
                "members": [
                    ["410000"],        # 1. Account
                    ["Total Entity"],  # 2. Entity
                    ["Actual"],        # 3. Scenario
                    ["FY25"],          # 4. Years
                    ["Dec"],           # 5. Period
                    ["YTD"],           # 6. View (trying YTD)
                    ["Working"],       # 7. Version
                    ["USD"],           # 8. Currency
                    ["No Future1"],    # 9. Future1
                    ["Total CostCenter"], # 10. CostCenter
                    ["Total Region"]   # 11. Region
                ]
            }
        },
        {
            "name": "11 dims: Account, Entity, Scenario, Years, Period, Version, Currency, Future1, CostCenter, Region, View",
            "pov": {
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
                    ["Total Region"],  # 10. Region
                    ["YTD"]            # 11. View (at end)
                ]
            }
        },
        {
            "name": "10 dims: No View, but try Period in View position",
            "pov": {
                "members": [
                    ["410000"],        # 1. Account
                    ["Total Entity"],  # 2. Entity
                    ["Actual"],        # 3. Scenario
                    ["FY25"],          # 4. Years
                    ["Dec"],           # 5. Period
                    ["Period"],        # 6. Try "Period" as View
                    ["Working"],       # 7. Version
                    ["USD"],           # 8. Currency
                    ["No Future1"],    # 9. Future1
                    ["Total CostCenter"], # 10. CostCenter
                    ["Total Region"]   # 11. Region (11 total)
                ]
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"Testing: {test_case['name']}")
        print('='*80)
        
        grid_definition = {
            "suppressMissingBlocks": True,
            "pov": test_case["pov"],
            "columns": [{"members": [["Dec"]]}],
            "rows": [{"members": [["410000"], ["Total CostCenter"], ["Total Region"]]}]
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
                            print(f"[ERROR] {detail_match.group(1)[:300]}")
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
    asyncio.run(test_with_view())




