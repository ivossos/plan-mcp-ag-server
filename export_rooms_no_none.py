"""Try without 'None' - use empty arrays or omit dimensions."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Try different approaches without 'None'."""
    await initialize_agent()
    
    # Try 1: Empty arrays instead of "None"
    grid_definition1 = {
        "suppressMissingBlocks": True,
        "pov": [
            ["410000"],
            ["FCCS_Total Geography"],
            ["Actual"],
            ["FY24"],
            ["Jan"],
            ["YTD"],
            [],  # ICP - empty
            [],  # Data Source - empty
            [],  # Movement - empty
            [],  # Multi-GAAP - empty
            []   # Consolidation - empty
        ],
        "columns": [
            ["Jan", "Feb", "Mar"]
        ],
        "rows": [
            ["410000"]
        ]
    }
    
    # Try 2: Only 6 dimensions (omit the optional ones)
    grid_definition2 = {
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
    
    for i, grid_def in enumerate([grid_definition1, grid_definition2], 1):
        print(f"\n{'='*60}")
        print(f"ATTEMPT {i}: {'Empty arrays' if i == 1 else 'Only 6 dimensions'}")
        print(f"{'='*60}")
        
        arguments = {
            "plan_type": "FinPlan",
            "grid_definition": grid_def
        }
        
        try:
            result = await execute_tool("export_data_slice", arguments)
            print(f"RESULT: {result.get('status')}")
            
            if result.get("status") == "success":
                print("SUCCESS!")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                with open("rooms_revenue_data.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                return result
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"Exception: {e}")
    
    return None

if __name__ == "__main__":
    asyncio.run(export_rooms_revenue())





