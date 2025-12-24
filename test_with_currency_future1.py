"""Test export_data_slice with Currency and Future1 dimensions."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_with_currency_future1():
    """Test with Currency and Future1 in POV"""
    config = load_config()
    client = PlanningClient(config)
    
    app_name = "PlanApp"
    plan_type = "FinPlan"
    
    # Test with Currency and Future1 included
    test_formats = [
        {
            "name": "Format 1: POV as array with Currency and Future1",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": [
                    ["410000"],        # Account
                    ["Total Entity"],  # Entity
                    ["Actual"],        # Scenario
                    ["FY25"],          # Years
                    ["Dec"],           # Period
                    ["USD"],           # Currency
                    ["No Future1"]     # Future1
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
            "name": "Format 2: POV as object with Currency and Future1",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"],
                        ["Total Entity"],
                        ["Actual"],
                        ["FY25"],
                        ["Dec"],
                        ["USD"],
                        ["No Future1"]
                    ]
                },
                "columns": [
                    ["Dec"]
                ],
                "rows": [
                    ["410000"]
                ]
            }
        }
    ]
    
    for test_format in test_formats:
        print(f"\n{test_format['name']}")
        print("=" * 80)
        print(json.dumps(test_format['grid_definition'], indent=2))
        print()
        
        try:
            result = await client.export_data_slice(
                app_name,
                plan_type,
                test_format['grid_definition']
            )
            print("[SUCCESS]")
            print(f"Result keys: {list(result.keys())}")
            if result.get("rows"):
                rows = result["rows"]
                print(f"Rows: {len(rows)}")
                if rows and rows[0].get("data"):
                    print(f"Data: {rows[0]['data']}")
            print(f"\nFull result:\n{json.dumps(result, indent=2, ensure_ascii=False)[:800]}")
            await client.close()
            return result
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR]: {error_msg[:300]}")
            if hasattr(e, 'response'):
                try:
                    error_text = await e.response.aread()
                    error_details = error_text.decode('utf-8', errors='ignore')
                    print(f"Error details: {error_details[:500]}")
                except:
                    pass
    
    await client.close()
    return None

if __name__ == "__main__":
    asyncio.run(test_with_currency_future1())




