"""Get top 10 products by revenue using the correct Planning format."""

import asyncio
import sys
import csv
from planning_agent.client.planning_client import PlanningClient
from planning_agent.config import load_config

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def get_top_10_products():
    config = load_config()
    client = PlanningClient(config)
    
    # Load all leaf-level revenue accounts from CSV
    revenue_accounts = []
    try:
        with open('ExportedMetadata_Account.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if row and len(row) > 5:
                    account_name = row[0].strip()
                    data_storage = row[5].strip() if len(row) > 5 else ''
                    # Get leaf-level (store) revenue accounts
                    if account_name and account_name.startswith('4') and len(account_name) == 6 and account_name.isdigit():
                        if data_storage.lower() == 'store':
                            revenue_accounts.append(account_name)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    # Remove duplicates and sort
    revenue_accounts = sorted(list(set(revenue_accounts)))
    
    print(f"Querying {len(revenue_accounts)} revenue accounts for top 10 by revenue...")
    
    # Use the CORRECT format: minimal POV, Period in columns, Account in rows
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["Total Entity"],  # Entity
                ["Actual"],        # Scenario
                ["FY25"],          # Years
                ["Working"],       # Version
                ["USD"],           # Currency
                ["No Future1"],    # Future1
                ["Total CostCenter"], # CostCenter
                ["Total Region"]   # Region
            ]
        },
        "columns": [
            {
                "dimensions": ["Period"],  # Note: "dimensions" plural!
                "members": [["Dec"]]
            }
        ],
        "rows": [
            {
                "dimensions": ["Account"],  # Note: "dimensions" plural!
                "members": [[acc]]
            }
            for acc in revenue_accounts
        ]
    }
    
    try:
        result = await client.export_data_slice("PlanApp", "FinPlan", grid_definition)
        print("[API Call Successful!]")
        
        # Process results
        rows = result.get("rows", [])
        print(f"Rows returned: {len(rows)}")
        
        # Extract revenue data
        revenue_data = []
        for row in rows:
            account = row.get("memberName") or row.get("member", "")
            data = row.get("data", [])
            if data and len(data) > 0:
                # Sum all values for this account
                total_revenue = sum(float(v) for v in data if v is not None)
                if total_revenue > 0:
                    revenue_data.append({
                        "account": account,
                        "revenue": total_revenue
                    })
        
        # Sort by revenue descending
        revenue_data.sort(key=lambda x: x["revenue"], reverse=True)
        
        # Get top 10
        top_10 = revenue_data[:10]
        
        print("\n" + "="*60)
        print("TOP 10 PRODUCTS BY REVENUE")
        print("="*60)
        
        if top_10:
            for i, item in enumerate(top_10, 1):
                print(f"{i:2d}. Account {item['account']:10s} - ${item['revenue']:,.2f}")
        else:
            print("No revenue data found for the specified POV.")
            print("\nPossible reasons:")
            print("  - Data hasn't been loaded yet")
            print("  - Data exists under different POV members (different entities/scenarios/years)")
            print("  - Accounts are dynamic calc and aggregate from child accounts")
            print("\nThe API format is correct - try querying with different POV members.")
        
        await client.close()
        return {"top_10": top_10, "total_accounts_queried": len(revenue_accounts)}
        
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR]: {error_msg}")
        if hasattr(e, 'response'):
            try:
                error_text = await e.response.aread()
                details = error_text.decode('utf-8', errors='ignore')
                import re
                detail_match = re.search(r'"detail":"([^"]+)"', details)
                if detail_match:
                    print(f"Details: {detail_match.group(1)[:500]}")
            except Exception:
                pass
        await client.close()
        return None

if __name__ == "__main__":
    result = asyncio.run(get_top_10_products())
    if result:
        print(f"\nQuery completed. Accounts queried: {result.get('total_accounts_queried', 0)}")

