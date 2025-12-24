"""Test using FCCS structure (columns/rows as arrays) but with Planning dimensions from CSV."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def test_fccs_structure():
    await initialize_agent()
    
    # Use FCCS STRUCTURE (columns/rows as arrays) but Planning DIMENSIONS (from CSV)
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["400000"],          # Account: Revenue
                ["Total Entity"],    # Entity (from CSV)
                ["Actual"],          # Scenario (from CSV)
                ["FY25"],            # Years (from CSV)
                ["Dec"],             # Period
                ["Working"],         # Version (from CSV)
                ["USD"],            # Currency (from CSV)
                ["No Future1"],      # Future1 (from CSV)
                ["Total CostCenter"], # CostCenter (from CSV)
                ["Total Region"]     # Region (from CSV)
            ]
        },
        "columns": [
            {
                "members": [["Dec"]]
            }
        ],
        "rows": [
            {
                "members": [["400000"], ["410000"], ["420000"], ["411000"], ["412000"], ["413000"], ["414000"], ["421000"], ["422000"], ["423000"], ["430000"], ["440000"]]
            }
        ]
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    print("="*60)
    print("TESTING: FCCS STRUCTURE + PLANNING DIMENSIONS")
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
            # Try to get detailed error
            error_detail = result.get('error', '')
            if 'detail' in error_detail.lower() or '400' in error_detail:
                print("\nTrying to get detailed error response...")
            return result
            
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_fccs_structure())

