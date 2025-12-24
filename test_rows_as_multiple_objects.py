"""Test rows as multiple dimension objects."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_multiple_row_objects():
    config = load_config()
    client = PlanningClient(config)
    
    # Try rows as multiple objects - one per dimension
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["410000"], ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]
            ]
        },
        "columns": [{"members": [["Dec"]]}],
        "rows": [
            {"members": [["410000"]]},           # Account
            {"members": [["Total Entity"]]},     # Entity
            {"members": [["Total CostCenter"]]}, # CostCenter
            {"members": [["Total Region"]]}      # Region
        ]
    }
    
    print("Testing rows as multiple dimension objects:")
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
                print(f"Details: {details[:500]}")
            except Exception:
                pass
        await client.close()
        return None

if __name__ == "__main__":
    asyncio.run(test_multiple_row_objects())




