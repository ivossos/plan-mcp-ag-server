"""Test with different entity names to see if that's the issue."""

import asyncio
import json
import sys
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_entities():
    config = load_config()
    client = PlanningClient(config)
    
    # Test different entity names
    entities_to_test = ["Total Entity", "All Entity", "E100"]
    
    for entity in entities_to_test:
        print(f"\n{'='*80}")
        print(f"Testing with entity: {entity}")
        print('='*80)
        
        grid_definition = {
            "suppressMissingBlocks": True,
            "pov": {
                "members": [
                    ["410000"],        # Account
                    [entity],          # Entity (testing different ones)
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
            "columns": [{"members": [["Dec"]]}],
            "rows": [{"members": [["410000"], ["Total CostCenter"], ["Total Region"]]}]
        }
        
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
                            full_error = detail_match.group(1)
                            print(f"[ERROR] {full_error}")
                            # Check if it mentions a specific dimension
                            if "dimension" in full_error.lower():
                                dim_match = re.search(r'dimension\s+(\w+)', full_error, re.IGNORECASE)
                                if dim_match:
                                    print(f"  -> Missing dimension: {dim_match.group(1)}")
                        else:
                            print(f"[ERROR] {details[:400]}")
                    else:
                        print(f"[ERROR] {details[:400]}")
                except Exception as ex:
                    print(f"[ERROR] {error_msg[:300]}")
                    print(f"  Exception parsing error: {ex}")
            else:
                print(f"[ERROR] {error_msg[:300]}")
    
    await client.close()
    return None

if __name__ == "__main__":
    asyncio.run(test_entities())




