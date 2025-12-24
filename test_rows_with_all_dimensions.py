"""Test rows with all dimensions specified, using 'dimensions' field."""

import asyncio
import json
import sys
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_all_dimensions_in_rows():
    config = load_config()
    client = PlanningClient(config)
    
    # Try with all dimensions in rows using "dimensions" field
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["410000"],        # Account
                ["Total Entity"],  # Entity
                ["Actual"],        # Scenario
                ["FY25"],          # Years
                ["Dec"],           # Period
                ["Working"],       # Version
                ["USD"],           # Currency
                ["No Future1"],    # Future1
                ["Total CostCenter"], # CostCenter
                ["Total Region"]   # Region
            ]
        },
        "columns": [
            {
                "dimensions": ["Period"],
                "members": [["Dec"]]
            }
        ],
        "rows": [
            {
                "dimensions": ["Account", "Entity", "Scenario", "Years", "Period", "Version", "Currency", "Future1", "CostCenter", "Region"],
                "members": [
                    ["410000"],        # Account
                    ["Total Entity"],  # Entity
                    ["Actual"],        # Scenario
                    ["FY25"],          # Years
                    ["Dec"],           # Period
                    ["Working"],       # Version
                    ["USD"],           # Currency
                    ["No Future1"],    # Future1
                    ["Total CostCenter"], # CostCenter
                    ["Total Region"]   # Region
                ]
            }
        ]
    }
    
    print("Testing with all dimensions in rows using 'dimensions' field:")
    print(json.dumps(grid_definition, indent=2))
    print()
    
    try:
        result = await client.export_data_slice("PlanApp", "FinPlan", grid_definition)
        print("[SUCCESS!]")
        print(f"Result keys: {list(result.keys())}")
        if result.get("rows"):
            rows = result["rows"]
            print(f"Rows returned: {len(rows)}")
            if rows and len(rows) > 0:
                print(f"First row: {json.dumps(rows[0], indent=2, ensure_ascii=False)}")
        print(f"\nFull result:\n{json.dumps(result, indent=2, ensure_ascii=False)[:1500]}")
        await client.close()
        return result
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR]: {error_msg}")
        if hasattr(e, 'response'):
            try:
                error_text = await e.response.aread()
                details = error_text.decode('utf-8', errors='ignore')
                # Extract detail message
                import re
                detail_match = re.search(r'"detail":"([^"]+)"', details)
                if detail_match:
                    print(f"Details: {detail_match.group(1)[:500]}")
                else:
                    print(f"Full error: {details[:800]}")
            except Exception as ex:
                print(f"Could not read error details: {ex}")
        await client.close()
        return None

if __name__ == "__main__":
    asyncio.run(test_all_dimensions_in_rows())

