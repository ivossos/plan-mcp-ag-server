"""Test with ALL dimensions in rows."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_all_dims():
    config = load_config()
    client = PlanningClient(config)
    
    # Try with ALL dimensions in rows
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
        "columns": [{"members": [["Dec"]]}],
        "rows": [{
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
        }]
    }
    
    print("Testing with ALL dimensions in rows:")
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
    asyncio.run(test_all_dims())




