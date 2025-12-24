"""Test script to export Rooms Revenue data from Planning application."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def test_export_rooms_revenue():
    """Test exporting Rooms Revenue (410000) data."""
    print("Initializing Planning agent...")
    await initialize_agent()
    print("Agent initialized successfully!")
    
    # Grid definition for Rooms Revenue
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["410000"],  # Account: Rooms Revenue
                ["FCCS_Total Geography"],  # Entity
                ["Actual"],  # Scenario
                ["FY24"],  # Years
                ["Jan"],  # Period
                ["YTD"],  # View
                ["None"],  # ICP
                ["None"],  # Data Source
                ["None"],  # Movement
                ["None"],  # Multi-GAAP
                ["None"]  # Consolidation
            ]
        },
        "columns": [
            {
                "members": [
                    ["Jan"], ["Feb"], ["Mar"], ["Apr"], 
                    ["May"], ["Jun"], ["Jul"], ["Aug"], 
                    ["Sep"], ["Oct"], ["Nov"], ["Dec"]
                ]
            }
        ],
        "rows": [
            {
                "members": [["410000"]]
            }
        ]
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    print("\nExporting Rooms Revenue data...")
    print(f"Plan Type: FinPlan")
    print(f"Account: 410000 (Rooms Revenue)")
    print(f"Grid Definition: {json.dumps(grid_definition, indent=2)}")
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        print("\n" + "="*50)
        print("EXPORT RESULT:")
        print("="*50)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_export_rooms_revenue())
    if result:
        print("\n✓ Export completed successfully!")
    else:
        print("\n✗ Export failed!")





