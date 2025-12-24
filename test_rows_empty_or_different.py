"""Test if rows should be empty or structured completely differently."""

import asyncio
import json
import sys
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_rows_variations():
    config = load_config()
    client = PlanningClient(config)
    
    # Base POV with 10 dimensions (no View)
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
    
    test_cases = [
        {
            "name": "Rows: Empty array",
            "rows": []
        },
        {
            "name": "Rows: Empty object",
            "rows": [{}]
        },
        {
            "name": "Rows: Account only (current)",
            "rows": [{"members": [["410000"]]}]
        },
        {
            "name": "Rows: Account + Entity (both base dims)",
            "rows": [{"members": [["410000"], ["Total Entity"]]}]
        },
        {
            "name": "Rows: Entity only",
            "rows": [{"members": [["Total Entity"]]}]
        },
        {
            "name": "Rows: CostCenter only",
            "rows": [{"members": [["Total CostCenter"]]}]
        },
        {
            "name": "Rows: Region only",
            "rows": [{"members": [["Total Region"]]}]
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
        
        print(f"Rows: {json.dumps(test_case['rows'], indent=2)}")
        
        try:
            result = await client.export_data_slice("PlanApp", "FinPlan", grid_definition)
            print("[SUCCESS!]")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:800])
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
                            error_detail = detail_match.group(1)
                            print(f"[ERROR] {error_detail[:250]}")
                            # Check for specific clues
                            if "row" in error_detail.lower():
                                print("  -> Row-related error")
                            if "dimension" in error_detail.lower():
                                print("  -> Dimension-related error")
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
    asyncio.run(test_rows_variations())




