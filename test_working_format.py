"""Test the working format: POV and columns/rows as objects with members."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_working():
    config = load_config()
    client = PlanningClient(config)
    
    # Format: POV as object, columns/rows as objects with members (no dimension field)
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["410000"],
                ["Total Entity"],
                ["Actual"],
                ["FY25"],
                ["Dec"]
            ]
        },
        "columns": {
            "members": [["Dec"]]
        },
        "rows": {
            "members": [["410000"]]
        }
    }
    
    print("Testing format: POV and columns/rows as objects with members")
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
    asyncio.run(test_working())




