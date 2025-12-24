"""Test different rows formats to find the correct one."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_rows_formats():
    config = load_config()
    client = PlanningClient(config)
    
    # POV is correct - test different rows formats
    base_pov = {
        "members": [
            ["410000"],
            ["Total Entity"],
            ["Actual"],
            ["FY25"],
            ["Dec"],
            ["Working"],
            ["USD"],
            ["No Future1"],
            ["Total CostCenter"],
            ["Total Region"]
        ]
    }
    
    test_formats = [
        {
            "name": "Rows as single array",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": base_pov,
                "columns": [{"members": [["Dec"]]}],
                "rows": [["410000"]]
            }
        },
        {
            "name": "Rows as array of arrays",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": base_pov,
                "columns": [{"members": [["Dec"]]}],
                "rows": [["410000"], ["Total Entity"]]
            }
        },
        {
            "name": "Rows as object with single member array",
            "grid_definition": {
                "suppressMissingBlocks": True,
                "pov": base_pov,
                "columns": [{"members": [["Dec"]]}],
                "rows": [{"members": [["410000"]]}]
            }
        }
    ]
    
    for test_format in test_formats:
        print(f"\n{test_format['name']}")
        print("=" * 80)
        
        try:
            result = await client.export_data_slice("PlanApp", "FinPlan", test_format['grid_definition'])
            print("[SUCCESS]")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:500])
            await client.close()
            return result
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR]: {error_msg[:300]}")
            if hasattr(e, 'response'):
                try:
                    error_text = await e.response.aread()
                    details = error_text.decode('utf-8', errors='ignore')
                    if "row" in details.lower():
                        print(f"Row-related error: {details[:400]}")
                except Exception:
                    pass
    
    await client.close()
    return None

if __name__ == "__main__":
    asyncio.run(test_rows_formats())




