"""Export Rooms Revenue data from Planning application using direct API call."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Export Rooms Revenue (410000) data."""
    await initialize_agent()
    
    # Grid definition for Planning REST API
    grid_definition = {
        "pov": {
            "members": [
                ["410000"],                    # Account: Rooms Revenue
                ["FCCS_Total Geography"],      # Entity: Total Geography
                ["Actual"],                    # Scenario: Actual
                ["FY24"],                      # Years: Fiscal Year 2024
                ["Jan"],                       # Period: January
                ["YTD"],                       # View: Year-to-Date
                ["None"],                      # ICP: None
                ["None"],                      # Data Source: None
                ["None"],                      # Movement: None
                ["None"],                      # Multi-GAAP: None
                ["None"]                       # Consolidation: None
            ]
        },
        "columns": [
            {
                "dimension": "Period",
                "members": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
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
    
    print("="*60)
    print("EXPORTING ROOMS REVENUE DATA")
    print("="*60)
    print("Account: 410000 (Rooms Revenue)")
    print("Plan Type: FinPlan")
    print("Entity: FCCS_Total Geography")
    print("Scenario: Actual")
    print("Years: FY24")
    print("Periods: Jan through Dec")
    print()
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        print("="*60)
        print("EXPORT RESULT:")
        print("="*60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save to file
        with open("rooms_revenue_export.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print("\nResult saved to: rooms_revenue_export.json")
        
        return result
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(export_rooms_revenue())
    if result and result.get("status") == "success":
        print("\n✓ Export completed successfully!")
    else:
        print("\n✗ Export failed!")





