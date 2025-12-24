"""Try with all 11 dimensions in correct order."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Try with all dimensions in order: Account, Entity, Period, Scenario, Years, View, ICP, Data Source, Movement, Multi-GAAP, Consolidation"""
    await initialize_agent()
    
    # All 11 dimensions in the order they appear in the application
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": [
            ["410000"],                    # 1. Account
            ["FCCS_Total Geography"],      # 2. Entity
            ["Jan"],                       # 3. Period (moved up)
            ["Actual"],                    # 4. Scenario
            ["FY24"],                      # 5. Years
            ["YTD"],                       # 6. View
            ["None"],                      # 7. ICP
            ["None"],                      # 8. Data Source
            ["None"],                      # 9. Movement
            ["None"],                      # 10. Multi-GAAP
            ["None"]                       # 11. Consolidation
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
    
    print("Trying all 11 dimensions in order...")
    print(f"POV order: Account, Entity, Period, Scenario, Years, View, ICP, Data Source, Movement, Multi-GAAP, Consolidation")
    
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
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(export_rooms_revenue())





