"""Test the exact format from rooms.docx document."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def test_rooms_format():
    await initialize_agent()
    
    # Planning format (NOT FCCS) - using dimensions from CSV files
    grid_definition = {
        "pov": {
            "members": [
                ["410000"],          # Account: Rooms Revenue
                ["Total Entity"],    # Entity: Total Entity (from CSV)
                ["Actual"],          # Scenario: Actual (from CSV)
                ["FY25"],            # Years: FY25 (from CSV)
                ["Dec"],             # Period: Dec
                ["Working"],         # Version: Working (from CSV)
                ["USD"],            # Currency: USD (from CSV)
                ["No Future1"],      # Future1: No Future1 (from CSV)
                ["Total CostCenter"], # CostCenter: Total CostCenter (from CSV)
                ["Total Region"]     # Region: Total Region (from CSV)
            ]
        },
        "columns": [
            {
                "dimension": "Period",
                "members": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            }
        ],
        "rows": [
            {
                "dimension": "Account",
                "members": ["410000", "420000", "411000", "412000", "413000", "414000", "421000", "422000", "423000", "430000", "440000"]
            }
        ]
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    print("="*60)
    print("TESTING FORMAT FROM rooms.docx")
    print("="*60)
    print(json.dumps(grid_definition, indent=2))
    print()
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        
        if result.get("status") == "success":
            data = result.get("data", {})
            rows = data.get("rows", [])
            
            print(f"[SUCCESS] Got {len(rows)} rows")
            
            # Extract and sort by revenue
            products = []
            for row in rows:
                account = row.get("memberName") or row.get("name") or "Unknown"
                row_data = row.get("data", [])
                revenue = row_data[0] if row_data and len(row_data) > 0 else None
                
                if revenue is not None and revenue != 0:
                    products.append({"account": account, "revenue": revenue})
            
            products.sort(key=lambda x: abs(x["revenue"]) if x["revenue"] else 0, reverse=True)
            
            print("\n" + "="*60)
            print("TOP 10 PRODUCTS BY REVENUE")
            print("="*60)
            print(f"{'Rank':<6} {'Account':<30} {'Revenue':>20}")
            print("-" * 60)
            
            for i, p in enumerate(products[:10], 1):
                rev = p["revenue"]
                rev_str = f"${rev:,.2f}" if isinstance(rev, (int, float)) else str(rev)
                print(f"{i:<6} {p['account']:<30} {rev_str:>20}")
            
            return result
        else:
            print(f"[ERROR] {result.get('error')}")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return None
            
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_rooms_format())

