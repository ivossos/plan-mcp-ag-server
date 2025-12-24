"""Try explicit dimension names in POV."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Try with explicit dimension structure."""
    await initialize_agent()
    
    # Try with explicit dimension structure
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "Account": ["410000"],
            "Entity": ["FCCS_Total Geography"],
            "Scenario": ["Actual"],
            "Years": ["FY24"],
            "Period": ["Jan"],
            "View": ["YTD"]
        },
        "columns": [
            {
                "dimension": "Period",
                "members": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
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
    
    print("Trying explicit dimension names in POV...")
    print(f"Grid:\n{json.dumps(grid_definition, indent=2)}")
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        print("\nRESULT:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get("status") == "success":
            with open("rooms_revenue_data.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print("\nSUCCESS! Data saved to rooms_revenue_data.json")
        
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(export_rooms_revenue())





