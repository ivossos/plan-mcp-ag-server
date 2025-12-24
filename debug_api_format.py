"""Debug the actual API call format to see what's wrong."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def debug_api_call():
    """Debug the actual API call format."""
    print("=" * 80)
    print("DEBUGGING API CALL FORMAT")
    print("=" * 80)
    print()
    
    config = load_config()
    client = PlanningClient(config)
    
    # Test different grid definition formats
    test_formats = [
        {
            "name": "Format 1: Simple list POV (from export_rooms_fy25.py)",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": [
                    ["410000"],
                    ["Total Entity"],
                    ["Actual"],
                    ["FY25"],
                    ["Dec"],
                    ["YTD"]
                ],
                "columns": [
                    ["Dec"]
                ],
                "rows": [
                    ["410000"]
                ]
            }
        },
        {
            "name": "Format 2: POV as object with members",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"],
                        ["Total Entity"],
                        ["Actual"],
                        ["FY25"],
                        ["Dec"],
                        ["YTD"]
                    ]
                },
                "columns": [
                    {
                        "members": [["Dec"]]
                    }
                ],
                "rows": [
                    {
                        "members": [["410000"]]
                    }
                ]
            }
        },
        {
            "name": "Format 3: Minimal - only required fields",
            "grid_definition": {
                "pov": [
                    ["410000"],
                    ["Total Entity"],
                    ["Actual"],
                    ["FY25"],
                    ["Dec"],
                    ["YTD"]
                ],
                "columns": [["Dec"]],
                "rows": [["410000"]]
            }
        }
    ]
    
    app_name = "PlanApp"
    plan_type = "FinPlan"
    
    for test_format in test_formats:
        print(f"\n{test_format['name']}")
        print("-" * 80)
        print(f"Grid Definition:\n{json.dumps(test_format['grid_definition'], indent=2)}")
        print()
        
        try:
            result = await client.export_data_slice(
                app_name,
                plan_type,
                test_format['grid_definition']
            )
            print("SUCCESS!")
            print(f"Result keys: {list(result.keys())}")
            if result.get("rows"):
                print(f"Rows: {len(result['rows'])}")
                if result['rows']:
                    print(f"First row: {result['rows'][0]}")
            else:
                print(f"Full result: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
        except Exception as e:
            print(f"ERROR: {e}")
            # Try to get more details
            if hasattr(e, 'response'):
                try:
                    error_text = await e.response.aread()
                    print(f"Error details: {error_text.decode('utf-8', errors='ignore')[:500]}")
                except Exception:
                    pass
        
        print()
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(debug_api_call())




