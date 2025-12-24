"""Export Rooms Revenue with simplified grid definition."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Export Rooms Revenue (410000) data with simplified grid."""
    await initialize_agent()
    
    # Simplified grid definition - Planning REST API format
    grid_definition = {
        "pov": ["410000", "FCCS_Total Geography", "Actual", "FY24", "Jan", "YTD"],
        "columns": [["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]],
        "rows": [["410000"]]
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    print("Exporting Rooms Revenue (410000)...")
    print(f"Grid Definition: {json.dumps(grid_definition, indent=2)}")
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        print("\nResult:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(export_rooms_revenue())





