"""Get top 10 products by revenue using Planning format (NOT FCCS format)."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def get_top_products():
    """Get top 10 products by revenue using Planning format."""
    await initialize_agent()
    
    # Planning format - NOT FCCS format
    # Dimensions: Account, Entity, Scenario, Years, Period, Version, Currency, Future1, CostCenter, Region
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["40000"],           # Account: Sales/Revenue
                ["Total Entity"],    # Entity
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
                "members": [
                    "40000", "40100", "40101", "40102", "40103",
                    "40104", "40105", "40106", "40200", "40210",
                    "40300", "40310", "40400", "40500"
                ]
            }
        ]
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    print("="*60)
    print("GETTING TOP 10 PRODUCTS BY REVENUE")
    print("Using Planning format (NOT FCCS format)")
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

