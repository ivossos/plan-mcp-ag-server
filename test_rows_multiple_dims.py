"""Test rows with multiple dimensions included."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_rows_multiple():
    config = load_config()
    client = PlanningClient(config)
    
    # Try rows with Account + other dimensions
    test_formats = [
        {
            "name": "Rows: Account + Entity",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"], ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                        ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]
                    ]
                },
                "columns": [{"members": [["Dec"]]}],
                "rows": [{"members": [["410000"], ["Total Entity"]]}]
            }
        },
        {
            "name": "Rows: Account + CostCenter + Region",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"], ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                        ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]
                    ]
                },
                "columns": [{"members": [["Dec"]]}],
                "rows": [{"members": [["410000"], ["Total CostCenter"], ["Total Region"]]}]
            }
        },
        {
            "name": "Rows: All dimensions from POV",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"], ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                        ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]
                    ]
                },
                "columns": [{"members": [["Dec"]]}],
                "rows": [{"members": [["410000"], ["Total Entity"], ["Total CostCenter"], ["Total Region"]]}]
            }
        }
    ]
    
    for test_format in test_formats:
        print(f"\n{test_format['name']}")
        print("-" * 80)
        
        try:
            result = await client.export_data_slice("PlanApp", "FinPlan", test_format['grid_definition'])
            print("[SUCCESS]")
            if result.get("rows"):
                rows = result["rows"]
                print(f"Rows returned: {len(rows)}")
                if rows and rows[0].get("data"):
                    print(f"Data: {rows[0]['data']}")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:600])
            await client.close()
            return result
        except Exception as e:
            error_msg = str(e)
            if "row" in error_msg.lower() or hasattr(e, 'response'):
                if hasattr(e, 'response'):
                    try:
                        error_text = await e.response.aread()
                        details = error_text.decode('utf-8', errors='ignore')
                        if "row" in details.lower():
                            print(f"Row error: {details[:300]}")
                        else:
                            print(f"Error: {details[:300]}")
                    except:
                        print(f"Error: {error_msg[:300]}")
                else:
                    print(f"Error: {error_msg[:300]}")
            else:
                print(f"Error: {error_msg[:200]}")
    
    await client.close()
    return None

if __name__ == "__main__":
    asyncio.run(test_rows_multiple())




