"""Test with correct dimension order from FinPlan app."""

import asyncio
import json
import sys
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_correct_order():
    config = load_config()
    client = PlanningClient(config)
    
    # Correct order from FinPlan app image:
    # Account, CostCenter, Currency, Entity, Future1, Period, Region, Scenario, Version, Years
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
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
        },
        "columns": [
            {
                "members": [["Dec"]]
            }
        ],
        "rows": [
            {
                "members": [["410000"]]
            }
        ]
    }
    
    print("Testing with CORRECT dimension order from FinPlan app:")
    print("1. Account")
    print("2. CostCenter")
    print("3. Currency")
    print("4. Entity")
    print("5. Future1")
    print("6. Period")
    print("7. Region")
    print("8. Scenario")
    print("9. Version")
    print("10. Years")
    print()
    print(json.dumps(grid_definition, indent=2))
    print()
    
    try:
        result = await client.export_data_slice("PlanApp", "FinPlan", grid_definition)
        print("[SUCCESS!]")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        await client.close()
        return result
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR]: {error_msg}")
        if hasattr(e, 'response'):
            try:
                error_text = await e.response.aread()
                details = error_text.decode('utf-8', errors='ignore')
                if "detail" in details:
                    import re
                    detail_match = re.search(r'"detail":"([^"]+)"', details)
                    if detail_match:
                        print(f"Detail: {detail_match.group(1)}")
                    else:
                        print(f"Details: {details[:500]}")
                else:
                    print(f"Details: {details[:500]}")
            except Exception:
                pass
        await client.close()
        return None

if __name__ == "__main__":
    asyncio.run(test_correct_order())




