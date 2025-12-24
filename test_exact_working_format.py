"""Test with exact format from working example, but using CSV entity names."""

import asyncio
import json
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

async def test_exact_format():
    """Test with exact format from export_rooms_revenue_planning.py"""
    config = load_config()
    client = PlanningClient(config)
    
    app_name = "PlanApp"
    plan_type = "FinPlan"
    
    # Test different entity names from CSV
    entity_names = ["Total Entity", "All Entity", "E100"]
    
    for entity in entity_names:
        print(f"\n{'='*80}")
        print(f"Testing with entity: {entity}")
        print('='*80)
        
        # Exact format from export_rooms_revenue_planning.py
        grid_definition = {
            "pov": {
                "members": [
                    ["410000"],           # Account
                    [entity],             # Entity (try different ones)
                    ["Actual"],           # Scenario
                    ["FY25"],            # Years
                    ["Dec"],             # Period
                    ["YTD"],             # View
                    ["None"],            # ICP
                    ["None"],            # Data Source
                    ["None"],            # Movement
                    ["None"],            # Multi-GAAP
                    ["None"]             # Consolidation
                ]
            },
            "columns": [
                {
                    "dimension": "Period",
                    "members": ["Dec"]  # Just Dec for testing
                }
            ],
            "rows": [
                {
                    "dimension": "Account",
                    "members": ["410000"]
                }
            ]
        }
        
        try:
            result = await client.export_data_slice(
                app_name,
                plan_type,
                grid_definition
            )
            print(f"[SUCCESS] with entity: {entity}")
            print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
            await client.close()
            return result
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] with entity {entity}: {error_msg}")
            
            # Try to get response details
            if hasattr(e, 'response'):
                try:
                    error_text = await e.response.aread()
                    error_details = error_text.decode('utf-8', errors='ignore')
                    print(f"Error details: {error_details[:500]}")
                except Exception:
                    pass
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(test_exact_format())




