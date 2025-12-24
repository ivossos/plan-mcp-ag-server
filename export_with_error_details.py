"""Export with detailed error information."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import PlanningConfig

async def export_with_details():
    """Export and capture full error details."""
    config = PlanningConfig()
    client = PlanningClient(config)
    await client.connect()
    
    app_name = "PlanApp"
    plan_type = "FinPlan"
    
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": [
            ["410000"],
            ["FCCS_Total Geography"],
            ["Actual"],
            ["FY24"],
            ["Jan"],
            ["YTD"]
        ],
        "columns": [
            ["Jan", "Feb", "Mar"]
        ],
        "rows": [
            ["410000"]
        ]
    }
    
    try:
        result = await client.export_data_slice(app_name, plan_type, grid_definition)
        print("SUCCESS!")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"ERROR: {type(e).__name__}")
        print(f"Message: {e}")
        # Try to get response details if it's an HTTP error
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            try:
                error_body = e.response.json()
                print(f"Error details: {json.dumps(error_body, indent=2)}")
            except Exception:
                print(f"Response text: {e.response.text}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(export_with_details())





