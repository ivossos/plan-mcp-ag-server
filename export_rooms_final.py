"""Final attempt to export Rooms Revenue with correct Planning API format."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Export Rooms Revenue (410000) data."""
    await initialize_agent()
    
    # Try Oracle Planning REST API v3 format - simpler structure
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": [
            ["410000"],                    # Account
            ["FCCS_Total Geography"],      # Entity  
            ["Actual"],                    # Scenario
            ["FY24"],                      # Years
            ["Jan"],                       # Period
            ["YTD"],                       # View
            ["None"],                      # ICP
            ["None"],                      # Data Source
            ["None"],                      # Movement
            ["None"],                      # Multi-GAAP
            ["None"]                       # Consolidation
        ],
        "columns": [
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        ],
        "rows": [
            ["410000"]
        ]
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    print("Exporting Rooms Revenue (410000)...")
    print(f"Grid Definition:\n{json.dumps(grid_definition, indent=2)}")
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        print("\n" + "="*60)
        print("RESULT:")
        print("="*60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get("status") == "success":
            with open("rooms_revenue_data.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print("\nData saved to: rooms_revenue_data.json")
        
        return result
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(export_rooms_revenue())





