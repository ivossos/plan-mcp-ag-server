"""Find where revenue data exists by trying different periods and parent accounts."""

import asyncio
import json
import sys
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def find_revenue_data():
    config = load_config()
    client = PlanningClient(config)
    
    # Try different approaches to find data
    test_cases = [
        {
            "name": "Parent account 400000 (Revenue) - Dec FY25",
            "pov": [["Total Entity"], ["Actual"], ["FY25"], ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]],
            "account": "400000",
            "period": "Dec"
        },
        {
            "name": "Parent account 410000 (Rooms Revenue) - Dec FY25",
            "pov": [["Total Entity"], ["Actual"], ["FY25"], ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]],
            "account": "410000",
            "period": "Dec"
        },
        {
            "name": "Parent account 400000 - Jan FY25",
            "pov": [["Total Entity"], ["Actual"], ["FY25"], ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]],
            "account": "400000",
            "period": "Jan"
        },
        {
            "name": "Parent account 400000 - All periods FY25",
            "pov": [["Total Entity"], ["Actual"], ["FY25"], ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]],
            "account": "400000",
            "period": None  # Will query all periods
        },
        {
            "name": "Parent account 400000 - FY24",
            "pov": [["Total Entity"], ["Actual"], ["FY24"], ["Working"], ["USD"], ["No Future1"], ["Total CostCenter"], ["Total Region"]],
            "account": "400000",
            "period": "Dec"
        }
    ]
    
    for test in test_cases:
        print(f"\n{'='*70}")
        print(f"Testing: {test['name']}")
        print('='*70)
        
        if test['period']:
            columns = [{"dimensions": ["Period"], "members": [[test['period']]]}]
        else:
            # Query all periods
            columns = [{"dimensions": ["Period"], "members": [["Jan"], ["Feb"], ["Mar"], ["Apr"], ["May"], ["Jun"], ["Jul"], ["Aug"], ["Sep"], ["Oct"], ["Nov"], ["Dec"]]}]
        
        grid_definition = {
            "suppressMissingBlocks": True,
            "pov": {"members": test['pov']},
            "columns": columns,
            "rows": [
                {
                    "dimensions": ["Account"],
                    "members": [[test['account']]]
                }
            ]
        }
        
        try:
            result = await client.export_data_slice("PlanApp", "FinPlan", grid_definition)
            rows = result.get("rows", [])
            
            if rows:
                print(f"[SUCCESS - Found {len(rows)} rows with data!]")
                for row in rows:
                    account = row.get("memberName") or row.get("member", "")
                    data = row.get("data", [])
                    if data:
                        total = sum(float(v) for v in data if v is not None)
                        print(f"  Account: {account}, Total: ${total:,.2f}")
                        print(f"  Data: {data}")
            else:
                print("[No data found]")
                
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, 'response'):
                try:
                    error_text = await e.response.aread()
                    details = error_text.decode('utf-8', errors='ignore')
                    import re
                    detail_match = re.search(r'"detail":"([^"]+)"', details)
                    if detail_match:
                        print(f"[ERROR] {detail_match.group(1)[:200]}")
                    else:
                        print(f"[ERROR] {error_msg[:200]}")
                except:
                    print(f"[ERROR] {error_msg[:200]}")
            else:
                print(f"[ERROR] {error_msg[:200]}")
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(find_revenue_data())

