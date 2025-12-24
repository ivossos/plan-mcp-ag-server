"""Get top 10 products by revenue using local CSV files for dimensions and hierarchies."""

import asyncio
import csv
import json
from pathlib import Path
from planning_agent.agent import initialize_agent, execute_tool

def load_accounts_from_csv():
    """Load account dimension from local CSV file."""
    csv_file = Path("ExportedMetadata_Account.csv")
    accounts = []
    
    if csv_file.exists():
        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    account_name = row.get("Account", "").strip()
                    parent = row.get("Parent", "").strip()
                    account_type = row.get("Account Type", "").strip()
                    
                    if account_name and account_name != "Account":
                        accounts.append({
                            "name": account_name,
                            "parent": parent if parent else "Root",
                            "account_type": account_type
                        })
        except Exception as e:
            print(f"Error loading accounts from CSV: {e}")
    
    return accounts

def find_revenue_accounts(accounts):
    """Find revenue-related accounts from the account list."""
    revenue_keywords = ["revenue", "sales", "income", "40000", "410000", "420000"]
    revenue_accounts = []
    
    for account in accounts:
        name_lower = account["name"].lower()
        if any(keyword in name_lower for keyword in revenue_keywords):
            revenue_accounts.append(account["name"])
    
    # Also look for accounts starting with 4 (typically revenue accounts)
    for account in accounts:
        if account["name"].isdigit() and account["name"].startswith("4"):
            if account["name"] not in revenue_accounts:
                revenue_accounts.append(account["name"])
    
    return revenue_accounts[:20]  # Limit to top 20 for testing

async def get_top_products():
    """Get top 10 products by revenue using Planning format and local CSV data."""
    await initialize_agent()
    
    # Load accounts from local CSV
    print("Loading accounts from local CSV file...")
    accounts = load_accounts_from_csv()
    print(f"Loaded {len(accounts)} accounts from CSV")
    
    # Find revenue accounts
    revenue_accounts = find_revenue_accounts(accounts)
    print(f"Found {len(revenue_accounts)} revenue-related accounts")
    print(f"Revenue accounts: {revenue_accounts[:10]}")
    
    if not revenue_accounts:
        print("No revenue accounts found. Using default accounts.")
        revenue_accounts = ["40000", "410000", "420000"]
    
    # Planning format - NOT FCCS format
    # Dimensions: Account, Entity, Scenario, Years, Period, Version, Currency, Future1, CostCenter, Region
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                [revenue_accounts[0] if revenue_accounts else "40000"],  # Account: First revenue account
                ["Total Entity"],    # Entity (from CSV)
                ["Actual"],          # Scenario
                ["FY25"],            # Years
                ["Dec"],             # Period
                ["Working"],         # Version
                ["USD"],            # Currency
                ["No Future1"],      # Future1
                ["Total CostCenter"], # CostCenter
                ["Total Region"]     # Region
            ]
        },
        "columns": [{"members": [["Dec"]]}],
        "rows": [
            {
                "dimension": "Account",
                "members": revenue_accounts[:15]  # Use revenue accounts from CSV
            }
        ]
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    print("\n" + "="*60)
    print("GETTING TOP 10 PRODUCTS BY REVENUE")
    print("Using Planning format (NOT FCCS format)")
    print("Using local CSV files for dimension data")
    print("="*60)
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        
        if result.get("status") == "success":
            data = result.get("data", {})
            rows = data.get("rows", [])
            
            products = []
            for row in rows:
                account = row.get("memberName") or row.get("name") or "Unknown"
                row_data = row.get("data", [])
                revenue = row_data[0] if row_data and len(row_data) > 0 else 0
                
                if revenue and revenue != 0:
                    products.append({"account": account, "revenue": revenue})
            
            products.sort(key=lambda x: abs(x["revenue"]) if x["revenue"] else 0, reverse=True)
            
            print("\nTOP 10 PRODUCTS BY REVENUE:")
            print("-" * 60)
            for i, p in enumerate(products[:10], 1):
                rev = p["revenue"]
                rev_str = f"${rev:,.2f}" if isinstance(rev, (int, float)) else str(rev)
                print(f"{i:2}. {p['account']:30} {rev_str:>15}")
            
            # Save results
            with open("top_products_revenue.json", "w", encoding="utf-8") as f:
                json.dump({
                    "top_10_products": products[:10],
                    "all_products": products,
                    "revenue_accounts_used": revenue_accounts
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\nResults saved to: top_products_revenue.json")
            return result
        else:
            print(f"Error: {result.get('error')}")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return None
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(get_top_products())

