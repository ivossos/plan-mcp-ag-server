"""Show top 10 products by revenue using local CSV files and Planning format."""

import asyncio
import csv
import json
from pathlib import Path
from planning_agent.agent import initialize_agent, execute_tool

def load_revenue_accounts_from_csv():
    """Load revenue accounts from local CSV file, including hierarchy."""
    csv_file = Path("ExportedMetadata_Account.csv")
    accounts = []
    revenue_accounts = []
    
    if not csv_file.exists():
        print(f"ERROR: CSV file not found: {csv_file}")
        print(f"Current directory: {Path.cwd()}")
        return []
    
    try:
        # Read CSV file - try utf-8 first, then utf-8-sig for BOM
        with open(csv_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            row_count = 0
            for row in reader:
                row_count += 1
                account_name = row.get("Account", "").strip()
                parent = row.get("Parent", "").strip()
                
                if account_name and account_name != "Account":
                    accounts.append({
                        "name": account_name,
                        "parent": parent if parent else "Root"
                    })
            
            print(f"Successfully read {row_count} rows from CSV")
        
        if not accounts:
            print("WARNING: Could not read CSV file with any encoding")
            return []
        
        print(f"Loaded {len(accounts)} total accounts from CSV")
        
        # Find revenue accounts: 400000 and all its descendants
        revenue_parents = ["400000", "410000", "420000", "430000", "440000"]
        found_revenue_parents = set()
        
        # First pass: find all revenue parent accounts
        for account in accounts:
            account_name = account["name"]
            if account_name in revenue_parents:
                found_revenue_parents.add(account_name)
                if account_name not in revenue_accounts:
                    revenue_accounts.append(account_name)
        
        # Second pass: find all children of revenue accounts
        # Keep expanding until we find all descendants
        changed = True
        while changed:
            changed = False
            for account in accounts:
                account_name = account["name"]
                parent = account["parent"]
                
                # If parent is a revenue account (or descendant), include this account
                if parent in found_revenue_parents:
                    if account_name not in revenue_accounts:
                        revenue_accounts.append(account_name)
                        found_revenue_parents.add(account_name)
                        changed = True
        
        # Also include any account starting with 4 that's numeric (revenue codes)
        for account in accounts:
            account_name = account["name"]
            if account_name.isdigit() and account_name.startswith("4") and len(account_name) >= 5:
                if account_name not in revenue_accounts:
                    revenue_accounts.append(account_name)
        
        # Sort accounts to maintain hierarchy order
        revenue_accounts.sort()
        
    except Exception as e:
        print(f"Error loading accounts from CSV: {e}")
        import traceback
        traceback.print_exc()
    
    return revenue_accounts

async def get_top_10_products():
    """Get top 10 products by revenue using Planning format."""
    await initialize_agent()
    
    # Load revenue accounts from local CSV
    print("="*60)
    print("LOADING REVENUE ACCOUNTS FROM LOCAL CSV FILE")
    print("="*60)
    revenue_accounts = load_revenue_accounts_from_csv()
    
    if not revenue_accounts:
        print("ERROR: No revenue accounts found in CSV file")
        return None
    
    print(f"Found {len(revenue_accounts)} revenue accounts")
    print(f"Sample accounts: {revenue_accounts[:10]}")
    
    # Use Planning format - NOT FCCS format
    # Start with known working accounts: 400000, 410000, 420000
    # Then expand to include their children
    known_working_accounts = ["400000", "410000", "420000", "411000", "412000", "413000", "414000", 
                              "421000", "422000", "423000", "430000", "440000"]
    
    # Filter to only include accounts that exist in our list
    accounts_to_query = [acc for acc in known_working_accounts if acc in revenue_accounts]
    
    if not accounts_to_query:
        # Fallback: use first few revenue accounts
        accounts_to_query = revenue_accounts[:10]
    
    print(f"\nUsing {len(accounts_to_query)} accounts: {accounts_to_query[:5]}...")
    
    # Based on test_working_format.py - simpler format that works
    # Rows format: each account needs to be wrapped in its own array
    account_rows = [[acc] for acc in accounts_to_query]
    
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["400000"],          # Account: Revenue (parent)
                ["Total Entity"],    # Entity
                ["Actual"],          # Scenario
                ["FY25"],            # Years
                ["Dec"]              # Period
                # Note: Only 5 dimensions in POV based on working test format
            ]
        },
        "columns": {
            "members": [["Dec"]]
        },
        "rows": {
            "members": account_rows  # Each account wrapped in its own array
        }
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    print("\n" + "="*60)
    print("QUERYING TOP 10 PRODUCTS BY REVENUE")
    print("Using Planning format (NOT FCCS format)")
    print("="*60)
    print(f"Querying {len(accounts_to_query)} revenue accounts...")
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        
        if result.get("status") == "success":
            data = result.get("data", {})
            rows = data.get("rows", [])
            
            print(f"\nReceived {len(rows)} rows of data")
            
            # Extract revenue values
            products = []
            for row in rows:
                account = row.get("memberName") or row.get("name") or "Unknown"
                row_data = row.get("data", [])
                
                # Get revenue value - could be in different formats
                revenue = None
                if row_data and len(row_data) > 0:
                    if isinstance(row_data[0], (int, float)):
                        revenue = row_data[0]
                    elif isinstance(row_data, list) and len(row_data) > 0:
                        revenue = row_data[0] if isinstance(row_data[0], (int, float)) else None
                
                if revenue is not None and revenue != 0:
                    products.append({
                        "account": account,
                        "revenue": revenue
                    })
            
            # Sort by absolute revenue value (descending)
            products.sort(key=lambda x: abs(x["revenue"]) if x["revenue"] else 0, reverse=True)
            
            # Display top 10
            print("\n" + "="*60)
            print("TOP 10 PRODUCTS BY REVENUE")
            print("="*60)
            print(f"{'Rank':<6} {'Account':<30} {'Revenue':>20}")
            print("-" * 60)
            
            for i, p in enumerate(products[:10], 1):
                rev = p["revenue"]
                if isinstance(rev, (int, float)):
                    rev_str = f"${rev:,.2f}"
                else:
                    rev_str = str(rev)
                print(f"{i:<6} {p['account']:<30} {rev_str:>20}")
            
            # Save results
            output_data = {
                "top_10_products": products[:10],
                "all_products": products,
                "total_products_found": len(products),
                "revenue_accounts_queried": revenue_accounts[:20]
            }
            
            with open("top_10_products_revenue.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print("\n[SUCCESS] Results saved to: top_10_products_revenue.json")
            print(f"[SUCCESS] Total products with revenue data: {len(products)}")
            
            return result
        else:
            print(f"\n[ERROR] Error: {result.get('error')}")
            print("\nFull error response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return None
            
    except Exception as e:
        print(f"\n[ERROR] Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TOP 10 PRODUCTS BY REVENUE")
    print("Using Local CSV Files + Planning Format")
    print("="*60 + "\n")
    
    result = asyncio.run(get_top_10_products())
    
    if result and result.get("status") == "success":
        print("\n" + "="*60)
        print("[SUCCESS] Query completed successfully!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("[FAILED] Query did not complete successfully")
        print("="*60)

