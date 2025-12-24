"""Test the correct API format based on error messages."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_correct_format():
    """Test with correct format based on API error messages."""
    print("=" * 80)
    print("TESTING CORRECT API FORMAT")
    print("=" * 80)
    print()
    
    config = load_config()
    client = PlanningClient(config)
    
    # Based on error: POV needs to be an object with "members" property
    # And "YTD" doesn't exist - let's try without View or with different View members
    test_formats = [
        {
            "name": "Format: POV as object, no View dimension",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"],      # Account
                        ["Total Entity"], # Entity
                        ["Actual"],       # Scenario
                        ["FY25"],        # Years
                        ["Dec"]          # Period (no View)
                    ]
                },
                "columns": {
                    "members": [["Dec"]]
                },
                "rows": {
                    "members": [["410000"]]
                }
            }
        },
        {
            "name": "Format: Try PeriodTotal as View",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"],
                        ["Total Entity"],
                        ["Actual"],
                        ["FY25"],
                        ["Dec"],
                        ["PeriodTotal"]  # Try PeriodTotal instead of YTD
                    ]
                },
                "columns": {
                    "members": [["Dec"]]
                },
                "rows": {
                    "members": [["410000"]]
                }
            }
        },
        {
            "name": "Format: Try YearTotal as View",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"],
                        ["Total Entity"],
                        ["Actual"],
                        ["FY25"],
                        ["Dec"],
                        ["YearTotal"]  # Try YearTotal
                    ]
                },
                "columns": {
                    "members": [["Dec"]]
                },
                "rows": {
                    "members": [["410000"]]
                }
            }
        },
        {
            "name": "Format: Try with all 12 months in columns",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"],
                        ["Total Entity"],
                        ["Actual"],
                        ["FY25"],
                        ["Jan"]  # Start with Jan
                    ]
                },
                "columns": {
                    "members": [["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
                },
                "rows": {
                    "members": [["410000"]]
                }
            }
        }
    ]
    
    app_name = "PlanApp"
    plan_type = "FinPlan"
    
    for test_format in test_formats:
        print(f"\n{test_format['name']}")
        print("-" * 80)
        
        try:
            result = await client.export_data_slice(
                app_name,
                plan_type,
                test_format['grid_definition']
            )
            print(f"[SUCCESS]")
            print(f"Result keys: {list(result.keys())}")
            
            if result.get("rows"):
                rows = result["rows"]
                print(f"Rows found: {len(rows)}")
                if rows and rows[0].get("data"):
                    data = rows[0]["data"]
                    print(f"Data values: {data}")
                    # Filter out None
                    valid_data = [v for v in data if v is not None]
                    if valid_data:
                        print(f"Valid values: {valid_data}")
                        print(f"Total: {sum(valid_data)}")
            else:
                print(f"Full result (first 500 chars):\n{json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
                
            # If successful, break
            break
            
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR]: {error_msg[:200]}")
            
            # Try to extract more details
            if "400" in error_msg or "Bad Request" in error_msg:
                # The error details were already shown in previous test
                pass
    
    await client.close()
    print("\n" + "=" * 80)

if __name__ == "__main__":
    asyncio.run(test_correct_format())

