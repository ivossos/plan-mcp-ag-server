"""Test export_data_slice with simple query, then expand to top 10 products."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def test_export():
    await initialize_agent()
    
    # Test 1: Single account (410000 - Rooms Revenue) - known working format
    print("="*60)
    print("TEST 1: Single Account (410000 - Rooms Revenue)")
    print("="*60)
    
    grid_definition_1 = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["410000"],
                ["Total Entity"],
                ["Actual"],
                ["FY25"],
                ["Dec"]
            ]
        },
        "columns": {
            "members": [["Dec"]]
        },
        "rows": {
            "members": [["410000"]]
        }
    }
    
    arguments_1 = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition_1
    }
    
    try:
        result_1 = await execute_tool("export_data_slice", arguments_1)
        print(f"Status: {result_1.get('status')}")
        
        if result_1.get("status") == "success":
            data = result_1.get("data", {})
            rows = data.get("rows", [])
            print(f"Rows returned: {len(rows)}")
            if rows:
                print(f"First row: {json.dumps(rows[0], indent=2, ensure_ascii=False)}")
            
            # Test 2: Multiple revenue accounts
            print("\n" + "="*60)
            print("TEST 2: Multiple Revenue Accounts (Top Products)")
            print("="*60)
            
            grid_definition_2 = {
                "suppressMissingBlocks": True,
                "pov": {
                    "members": [
                        ["400000"],  # Revenue parent
                        ["Total Entity"],
                        ["Actual"],
                        ["FY25"],
                        ["Dec"]
                    ]
                },
                "columns": {
                    "members": [["Dec"]]
                },
                "rows": {
                    "members": [
                        ["400000"],  # Revenue
                        ["410000"],  # Rooms Revenue
                        ["420000"],  # F&B Revenue
                        ["411000"],  # Transient Rooms Revenue
                        ["412000"],  # Group Rooms Revenue
                        ["413000"],  # Contract Rooms Revenue
                        ["414000"],  # Other Rooms Revenue
                        ["421000"],  # F&B Revenue - Food
                        ["422000"],  # F&B Revenue - Beverage
                        ["423000"],  # F&B Revenue - Other
                        ["430000"],  # Other Operated Revenue
                        ["440000"]   # Miscellaneous Income
                    ]
                }
            }
            
            arguments_2 = {
                "plan_type": "FinPlan",
                "grid_definition": grid_definition_2
            }
            
            result_2 = await execute_tool("export_data_slice", arguments_2)
            
            if result_2.get("status") == "success":
                data_2 = result_2.get("data", {})
                rows_2 = data_2.get("rows", [])
                
                print(f"Rows returned: {len(rows_2)}")
                
                # Extract and sort by revenue
                products = []
                for row in rows_2:
                    account = row.get("memberName") or row.get("name") or "Unknown"
                    row_data = row.get("data", [])
                    revenue = row_data[0] if row_data and len(row_data) > 0 else None
                    
                    if revenue is not None and revenue != 0:
                        products.append({
                            "account": account,
                            "revenue": revenue
                        })
                
                # Sort by absolute revenue (descending)
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
                with open("top_10_products_result.json", "w", encoding="utf-8") as f:
                    json.dump({
                        "top_10_products": products[:10],
                        "all_products": products
                    }, f, indent=2, ensure_ascii=False)
                
                print("\n[SUCCESS] Results saved to: top_10_products_result.json")
                return result_2
            else:
                print(f"[ERROR] Test 2 failed: {result_2.get('error')}")
                return result_2
        else:
            print(f"[ERROR] Test 1 failed: {result_1.get('error')}")
            print(json.dumps(result_1, indent=2, ensure_ascii=False))
            return result_1
            
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING export_data_slice")
    print("="*60 + "\n")
    
    result = asyncio.run(test_export())
    
    if result and result.get("status") == "success":
        print("\n" + "="*60)
        print("[SUCCESS] All tests passed!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("[FAILED] Tests did not complete successfully")
        print("="*60)

