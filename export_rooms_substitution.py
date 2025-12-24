"""Try using substitution variables for current period/year."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_rooms_revenue():
    """Try with substitution variables."""
    await initialize_agent()
    
    # Get substitution variables first
    try:
        vars_result = await execute_tool("get_substitution_variables", {})
        print("Substitution Variables:")
        print(json.dumps(vars_result, indent=2))
    except Exception:
        print("Could not get substitution variables")
    
    # Try with common member names that might exist
    # Maybe "Actual" should be "Plan" or "Budget" or something else
    # Maybe "FY24" should be "FY2024" or just "2024"
    # Maybe "YTD" should be "YTDTotal" or "YearTotal"
    
    test_configs = [
        {
            "name": "Standard names",
            "scenario": "Actual",
            "year": "FY24",
            "period": "Jan",
            "view": "YTD"
        },
        {
            "name": "Alternative scenario",
            "scenario": "Plan",
            "year": "FY24",
            "period": "Jan",
            "view": "YTD"
        },
        {
            "name": "Alternative year format",
            "scenario": "Actual",
            "year": "FY2024",
            "period": "Jan",
            "view": "YTD"
        }
    ]
    
    for config in test_configs:
        print(f"\n{'='*60}")
        print(f"Trying: {config['name']}")
        print(f"{'='*60}")
        
        grid_definition = {
            "suppressMissingBlocks": True,
            "pov": [
                ["410000"],
                ["FCCS_Total Geography"],
                [config["scenario"]],
                [config["year"]],
                [config["period"]],
                [config["view"]]
            ],
            "columns": [
                ["Jan"]
            ],
            "rows": [
                ["410000"]
            ]
        }
        
        arguments = {
            "plan_type": "FinPlan",
            "grid_definition": grid_definition
        }
        
        try:
            result = await execute_tool("export_data_slice", arguments)
            if result.get("status") == "success":
                print("SUCCESS!")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return result
            else:
                print(f"Failed: {result.get('error', 'Unknown')[:100]}")
        except Exception as e:
            print(f"Exception: {e}")
    
    return None

if __name__ == "__main__":
    asyncio.run(export_rooms_revenue())





