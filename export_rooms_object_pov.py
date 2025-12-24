"""Try POV as object with dimension names as keys."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Try POV as object mapping dimensions to members."""
    await initialize_agent()
    
    # POV as object with dimension names
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "Account": ["410000"],
            "Entity": ["FCCS_Total Geography"],
            "Scenario": ["Actual"],
            "Years": ["FY25"],
            "Period": ["May"],
            "View": ["YTD"]
        },
        "columns": [
            {
                "dimension": "Period",
                "members": ["Jan", "Feb", "Mar", "Apr", "May"]
            }
        ],
        "rows": [
            {
                "dimension": "Account",
                "members": ["410000"]
            }
        ]
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    print("Trying POV as object with dimension names...")
    print(json.dumps(grid_definition, indent=2))
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        print("\nRESULT:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get("status") == "success":
            print("\nSUCCESS!")
            with open("rooms_revenue_data.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            return result
    except Exception as e:
        print(f"Exception: {e}")
    
    return None

if __name__ == "__main__":
    asyncio.run(export_rooms_revenue())





