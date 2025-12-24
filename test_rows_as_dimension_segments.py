"""Test rows as dimension segments - maybe rows need to specify dimensions differently."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_dimension_segments():
    config = load_config()
    client = PlanningClient(config)
    
    # The error says "at least one dimension is not present on the row"
    # Maybe rows need to be structured as dimension segments?
    # Let's try different structures
    
    test_cases = [
        {
            "name": "Rows as array of dimension segments (each segment is a dimension)",
            "grid": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"], ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                        ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]
                    ]
                },
                "columns": [{"members": [["Dec"]]}],
                "rows": [
                    {"members": [["410000"]]},  # Account dimension segment
                    {"members": [["Total Entity"]]},  # Entity dimension segment
                    {"members": [["Total CostCenter"]]},  # CostCenter dimension segment
                    {"members": [["Total Region"]]}  # Region dimension segment
                ]
            }
        },
        {
            "name": "Rows with Account dimension only (single segment)",
            "grid": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                        ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]
                    ]
                },
                "columns": [{"members": [["Dec"]]}],
                "rows": [
                    {"members": [["410000"], ["420000"], ["411000"]]}  # Multiple accounts in one segment
                ]
            }
        },
        {
            "name": "Rows with Account + CostCenter + Region (3 segments)",
            "grid": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                        ["Working"], ["USD"], ["No Future1"]
                    ]
                },
                "columns": [{"members": [["Dec"]]}],
                "rows": [
                    {"members": [["410000"], ["420000"]]},  # Account segment
                    {"members": [["Total CostCenter"]]},  # CostCenter segment
                    {"members": [["Total Region"]]}  # Region segment
                ]
            }
        },
        {
            "name": "Rows with all 10 dimensions as separate segments",
            "grid": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": []  # Empty POV - all in rows
                },
                "columns": [{"members": [["Dec"]]}],
                "rows": [
                    {"members": [["410000"]]},  # Account
                    {"members": [["Total Entity"]]},  # Entity
                    {"members": [["Actual"]]},  # Scenario
                    {"members": [["FY25"]]},  # Years
                    {"members": [["Dec"]]},  # Period
                    {"members": [["Working"]]},  # Version
                    {"members": [["USD"]]},  # Currency
                    {"members": [["No Future1"]]},  # Future1
                    {"members": [["Total CostCenter"]]},  # CostCenter
                    {"members": [["Total Region"]]}  # Region
                ]
            }
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}: {test['name']}")
        print('='*70)
        
        try:
            result = await client.export_data_slice("PlanApp", "FinPlan", test["grid"])
            print("[SUCCESS!]")
            print(f"Result keys: {list(result.keys())}")
            if result.get("rows"):
                rows = result["rows"]
                print(f"Rows returned: {len(rows)}")
                if rows and len(rows) > 0:
                    print(f"First row: {rows[0]}")
            print(f"\nFull result:\n{json.dumps(result, indent=2, ensure_ascii=False)[:1000]}")
            await client.close()
            return result
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response'):
                try:
                    error_text = await e.response.aread()
                    details = error_text.decode('utf-8', errors='ignore')
                    # Extract detail message
                    import re
                    detail_match = re.search(r'"detail":"([^"]+)"', details)
                    if detail_match:
                        print(f"[ERROR] {detail_match.group(1)[:400]}")
                    else:
                        # Try to find error message
                        error_match = re.search(r'"message":"([^"]+)"', details)
                        if error_match:
                            print(f"[ERROR] {error_match.group(1)[:400]}")
                        else:
                            print(f"[ERROR] {details[:400]}")
                except Exception:
                    print(f"[ERROR] {error_msg[:300]}")
            else:
                print(f"[ERROR] {error_msg[:300]}")
    
    await client.close()
    return None

if __name__ == "__main__":
    asyncio.run(test_dimension_segments())

