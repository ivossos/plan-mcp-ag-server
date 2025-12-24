"""Export with correct year from substitution variables: FY25."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Export Rooms Revenue with FY25 (current year from substitution variables)."""
    await initialize_agent()
    
    # Use FY25 (current year from substitution variables) and May (current month)
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": [
            ["410000"],                    # Account
            ["FCCS_Total Geography"],      # Entity
            ["Actual"],                    # Scenario
            ["FY25"],                      # Years - CORRECTED from FY24 to FY25!
            ["May"],                       # Period - using current month
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
    
    print("="*60)
    print("EXPORTING ROOMS REVENUE WITH FY25")
    print("="*60)
    print("Account: 410000")
    print("Entity: FCCS_Total Geography")
    print("Scenario: Actual")
    print("Years: FY25 (from substitution variables)")
    print("Period: May (current month)")
    print("View: YTD")
    print()
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        print("RESULT:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get("status") == "success":
            print("\n" + "="*60)
            print("SUCCESS! Data exported successfully!")
            print("="*60)
            with open("rooms_revenue_data.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print("Data saved to: rooms_revenue_data.json")
        else:
            print(f"\nError: {result.get('error', 'Unknown error')}")
        
        return result
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(export_rooms_revenue())





