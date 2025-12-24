"""Systematically test different formats to find the working one."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_formats():
    config = load_config()
    client = PlanningClient(config)
    
    # Test different formats systematically
    test_cases = [
        {
            "name": "Format 1: Columns/rows as arrays, rows with dimension",
            "grid": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"], ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                        ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]
                    ]
                },
                "columns": [
                    {"members": [["Dec"]]}
                ],
                "rows": [
                    {
                        "dimension": "Account",
                        "members": [["410000"]]
                    }
                ]
            }
        },
        {
            "name": "Format 2: Columns/rows as arrays, rows without dimension",
            "grid": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"], ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                        ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]
                    ]
                },
                "columns": [
                    {"members": [["Dec"]]}
                ],
                "rows": [
                    {"members": [["410000"]]}
                ]
            }
        },
        {
            "name": "Format 3: Columns with dimension, rows without",
            "grid": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"], ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                        ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]
                    ]
                },
                "columns": [
                    {"dimension": "Period", "members": [["Dec"]]}
                ],
                "rows": [
                    {"members": [["410000"]]}
                ]
            }
        },
        {
            "name": "Format 4: Both columns and rows with dimension",
            "grid": {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["410000"], ["Total Entity"], ["Actual"], ["FY25"], ["Dec"],
                        ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]
                    ]
                },
                "columns": [
                    {"dimension": "Period", "members": [["Dec"]]}
                ],
                "rows": [
                    {"dimension": "Account", "members": [["410000"]]}
                ]
            }
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {test['name']}")
        print('='*60)
        
        try:
            result = await client.export_data_slice("PlanApp", "FinPlan", test["grid"])
            print("[SUCCESS!]")
            print(f"Result keys: {list(result.keys())}")
            if result.get("rows"):
                rows = result["rows"]
                print(f"Rows returned: {len(rows)}")
                if rows and rows[0].get("data"):
                    print(f"Data: {rows[0]['data']}")
            print(f"\nFull result:\n{json.dumps(result, indent=2, ensure_ascii=False)[:800]}")
            await client.close()
            return result
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response'):
                try:
                    error_text = await e.response.aread()
                    details = error_text.decode('utf-8', errors='ignore')
                    if "detail" in details:
                        import re
                        detail_match = re.search(r'"detail":"([^"]+)"', details)
                        if detail_match:
                            print(f"[ERROR] {detail_match.group(1)[:200]}")
                        else:
                            print(f"[ERROR] {details[:300]}")
                    else:
                        print(f"[ERROR] {details[:300]}")
                except Exception:
                    print(f"[ERROR] {error_msg[:300]}")
            else:
                print(f"[ERROR] {error_msg[:300]}")
    
    await client.close()
    return None

if __name__ == "__main__":
    asyncio.run(test_formats())

