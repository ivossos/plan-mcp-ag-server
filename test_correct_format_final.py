"""Test the correct format: POV as object, columns/rows as array of objects."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_correct():
    config = load_config()
    client = PlanningClient(config)
    
    # Correct format: Include ALL required dimensions
    # Order: Account, Entity, Scenario, Years, Period, Version, Currency, Future1, CostCenter, Region
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["410000"],        # Account
                ["Total Entity"],  # Entity
                ["Actual"],        # Scenario
                ["FY25"],          # Years
                ["Dec"],           # Period
                ["Working"],       # Version
                ["USD"],           # Currency
                ["No Future1"],    # Future1
                ["Total CostCenter"], # CostCenter
                ["Total Region"]   # Region
            ]
        },
        "columns": [
            {
                "members": [["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
            }
        ],
        "rows": [
            {
                "members": [["410000"]]
            }
        ]
    }
    
    print("Testing correct format:")
    print("POV: object with members")
    print("Columns: array of objects with members")
    print("Rows: array of objects with members")
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
                print(f"Details: {error_text.decode('utf-8', errors='ignore')}")
            except Exception:
                pass
        await client.close()
        return None

if __name__ == "__main__":
    asyncio.run(test_correct())

