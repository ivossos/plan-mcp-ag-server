"""Systematically test different row formats to find the correct one."""

import asyncio
import json
import sys
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_systematic():
    config = load_config()
    client = PlanningClient(config)
    
    # Base POV with 10 dimensions - this is correct
    base_pov = {
        "members": [
            ["410000"],        # 1. Account
            ["Total Entity"],  # 2. Entity
            ["Actual"],        # 3. Scenario
            ["FY25"],          # 4. Years
            ["Dec"],           # 5. Period
            ["Working"],       # 6. Version
            ["USD"],           # 7. Currency
            ["No Future1"],    # 8. Future1
            ["Total CostCenter"], # 9. CostCenter
            ["Total Region"]   # 10. Region
        ]
    }
    
    # Test different row formats
    test_cases = [
        {
            "name": "Rows: Only Account (current)",
            "rows": [{"members": [["410000"]]}]
        },
        {
            "name": "Rows: Account + CostCenter",
            "rows": [{"members": [["410000"], ["Total CostCenter"]]}]
        },
        {
            "name": "Rows: Account + Region",
            "rows": [{"members": [["410000"], ["Total Region"]]}]
        },
        {
            "name": "Rows: Account + CostCenter + Region",
            "rows": [{"members": [["410000"], ["Total CostCenter"], ["Total Region"]]}]
        },
        {
            "name": "Rows: Account + Entity",
            "rows": [{"members": [["410000"], ["Total Entity"]]}]
        },
        {
            "name": "Rows: Multiple row objects - Account only",
            "rows": [{"members": [["410000"]]}, {"members": [["Total CostCenter"]]}]
        },
        {
            "name": "Rows: Account + Entity + CostCenter + Region",
            "rows": [{"members": [["410000"], ["Total Entity"], ["Total CostCenter"], ["Total Region"]]}]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"Testing: {test_case['name']}")
        print('='*80)
        
        grid_definition = {
            "suppressMissingBlocks": True,
            "pov": base_pov,
            "columns": [{"members": [["Dec"]]}],
            "rows": test_case["rows"]
        }
        
        try:
            result = await client.export_data_slice("PlanApp", "FinPlan", grid_definition)
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
                    # Extract the detail message
                    if "detail" in details:
                        import re
                        detail_match = re.search(r'"detail":"([^"]+)"', details)
                        if detail_match:
                            print(f"[ERROR] {detail_match.group(1)[:200]}")
                        else:
                            print(f"[ERROR] {details[:300]}")
                    else:
                        print(f"[ERROR] {details[:300]}")
                except:
                    print(f"[ERROR] {error_msg[:300]}")
            else:
                print(f"[ERROR] {error_msg[:300]}")
    
    await client.close()
    return None

if __name__ == "__main__":
    asyncio.run(test_systematic())

