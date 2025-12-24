"""Try Oracle Planning REST API v3 exact format."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Try Oracle Planning REST API v3 format exactly."""
    await initialize_agent()
    
    # Oracle Planning REST API v3 format - POV with "members" key
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["410000"],                    # Account
                ["FCCS_Total Geography"],      # Entity
                ["Actual"],                    # Scenario
                ["FY25"],                      # Years
                ["May"],                       # Period
                ["YTD"],                       # View
                ["None"],                      # ICP
                ["None"],                      # Data Source
                ["None"],                      # Movement
                ["None"],                      # Multi-GAAP
                ["None"]                       # Consolidation
            ]
        },
        "columns": [
            {
                "members": [["Jan"], ["Feb"], ["Mar"], ["Apr"], ["May"], ["Jun"], ["Jul"], ["Aug"], ["Sep"], ["Oct"], ["Nov"], ["Dec"]]
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
    
    print("Trying Oracle Planning REST API v3 format...")
    print(json.dumps(grid_definition, indent=2))
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        print("\nRESULT:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get("status") == "success":
            print("\n" + "="*60)
            print("SUCCESS! ROOMS REVENUE DATA EXPORTED!")
            print("="*60)
            with open("rooms_revenue_data.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print("Data saved to: rooms_revenue_data.json")
            return result
        else:
            print(f"\nStill error: {result.get('error', 'Unknown')[:200]}")
    except Exception as e:
        print(f"Exception: {e}")
    
    return None

if __name__ == "__main__":
    asyncio.run(export_rooms_revenue())





