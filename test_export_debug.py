"""Debug export_data_slice to get detailed error information."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def debug_export():
    config = load_config()
    client = PlanningClient(config)
    
    # Fixed format: columns and rows must be ARRAYS, not objects!
    # ALL 10 dimensions required: Account, Entity, Scenario, Years, Period, Version, Currency, Future1, CostCenter, Region
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["410000"],          # Account
                ["Total Entity"],    # Entity
                ["Actual"],          # Scenario
                ["FY25"],            # Years
                ["Dec"],             # Period
                ["Working"],         # Version
                ["USD"],            # Currency
                ["No Future1"],      # Future1
                ["Total CostCenter"], # CostCenter
                ["Total Region"]     # Region
            ]
        },
        "columns": [
            {
                "members": [["Dec"]]
            }
        ],
        "rows": [
            {
                "members": [
                    ["410000"],        # Account
                    ["Total Entity"],  # Entity
                    ["Actual"],        # Scenario
                    ["FY25"],          # Years
                    ["Dec"],           # Period
                    ["Working"],       # Version
                    ["USD"],          # Currency
                    ["No Future1"],    # Future1
                    ["Total CostCenter"], # CostCenter
                    ["Total Region"]   # Region
                ]
            }
        ]
    }
    
    print("Testing export_data_slice with:")
    print(json.dumps(grid_definition, indent=2))
    print()
    
    try:
        result = await client.export_data_slice("PlanApp", "FinPlan", grid_definition)
        print("[SUCCESS]")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        await client.close()
        return result
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR]: {error_msg}")
        
        # Try to get detailed error response
        if hasattr(e, 'response'):
            try:
                error_text = await e.response.aread()
                error_details = error_text.decode('utf-8', errors='ignore')
                print("\nDetailed Error Response:")
                print("="*60)
                print(error_details)
                print("="*60)
                
                # Try to parse as JSON
                try:
                    error_json = json.loads(error_details)
                    print("\nParsed Error JSON:")
                    print(json.dumps(error_json, indent=2, ensure_ascii=False))
                except Exception:
                    pass
            except Exception as ex:
                print(f"Could not read error details: {ex}")
        
        await client.close()
        return None

if __name__ == "__main__":
    asyncio.run(debug_export())

