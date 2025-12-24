"""Minimal grid definition - only essential dimensions."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Export Rooms Revenue with minimal grid definition."""
    await initialize_agent()
    
    # Minimal grid - only Account, Entity, Scenario, Years, Period, View
    # Remove ICP, Data Source, Movement, Multi-GAAP, Consolidation
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": [
            ["410000"],                    # Account
            ["FCCS_Total Geography"],      # Entity  
            ["Actual"],                    # Scenario
            ["FY24"],                      # Years
            ["Jan"],                       # Period
            ["YTD"]                        # View
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
    
    print("Trying minimal grid definition (6 dimensions only)...")
    print(f"Grid:\n{json.dumps(grid_definition, indent=2)}")
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        print("\nRESULT:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(export_rooms_revenue())





