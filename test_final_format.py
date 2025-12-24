"""Test final correct format - columns/rows as arrays, not dimension objects."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_final_format():
    """Test with correct format: columns/rows as arrays"""
    config = load_config()
    client = PlanningClient(config)
    
    app_name = "PlanApp"
    plan_type = "FinPlan"
    
    # Correct format: columns and rows as arrays of member arrays
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["410000"],        # Account
                ["Total Entity"],  # Entity
                ["Actual"],        # Scenario
                ["FY25"],          # Years
                ["Dec"]            # Period
            ]
        },
        "columns": [
            ["Dec"]  # Just Dec for testing
        ],
        "rows": [
            ["410000"]
        ]
    }
    
    print("Testing final format (columns/rows as arrays):")
    print(json.dumps(grid_definition, indent=2))
    print()
    
    try:
        result = await client.export_data_slice(
            app_name,
            plan_type,
            grid_definition
        )
        print("[SUCCESS]")
        print(f"Result keys: {list(result.keys())}")
        if result.get("rows"):
            rows = result["rows"]
            print(f"Rows: {len(rows)}")
            if rows and rows[0].get("data"):
                print(f"Data: {rows[0]['data']}")
        print(f"\nFull result:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
        await client.close()
        return result
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR]: {error_msg}")
        if hasattr(e, 'response'):
            try:
                error_text = await e.response.aread()
                error_details = error_text.decode('utf-8', errors='ignore')
                print(f"Error details: {error_details}")
            except Exception:
                pass
        await client.close()
        return None

if __name__ == "__main__":
    asyncio.run(test_final_format())




