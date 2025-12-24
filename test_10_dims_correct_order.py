"""Test with exactly 10 dimensions in correct order."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_10_dims():
    config = load_config()
    client = PlanningClient(config)
    
    # 10 dimensions in order: Account, Entity, Scenario, Years, Period, Version, Currency, Future1, CostCenter, Region
    grid_definition = {
        "suppressMissingBlocks": True,
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
                ["Total Region"]   # 10. Region
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
    
    print("Testing with exactly 10 dimensions:")
    print("1. Account")
    print("2. Entity")
    print("3. Scenario")
    print("4. Years")
    print("5. Period")
    print("6. Version")
    print("7. Currency")
    print("8. Future1")
    print("9. CostCenter")
    print("10. Region")
    print()
    print(json.dumps(grid_definition, indent=2))
    print()
    
    try:
        result = await client.export_data_slice("PlanApp", "FinPlan", grid_definition)
        print("[SUCCESS]")
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
                print(f"Details: {details}")
            except:
                pass
        await client.close()
        return None

if __name__ == "__main__":
    asyncio.run(test_10_dims())




