"""Export top 10 products by revenue from Planning application."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def export_top_products_revenue():
    """Export revenue data to identify top products."""
    await initialize_agent()
    
    # Use the exact format from the working example, but query for Sales revenue
    # Try with account 40000 (Sales) which exists in the account list
    grid_definition = {
        "pov": {
            "members": [
                ["40000"],                   # Account: Sales (revenue account code)
                ["FCCS_Total Geography"],    # Entity: Total Geography
                ["Actual"],                  # Scenario: Actual
                ["FY24"],                    # Years: Fiscal Year 2024
                ["Dec"],                     # Period: December
                ["YTD"],                     # View: Year-to-Date
                ["None"],                    # ICP: None
                ["None"],                    # Data Source: None
                ["None"],                    # Movement: None
                ["None"],                    # Multi-GAAP: None
                ["None"]                     # Consolidation: None
            ]
        },
        "columns": [
            {
                "dimension": "Period",
                "members": ["Dec"]
            }
        ],
        "rows": [
            {
                "dimension": "Account",
                "members": [
                    "40000",
                    "40100",
                    "40101",
                    "40102",
                    "40103",
                    "40104",
                    "40105",
                    "40106",
                    "40200",
                    "40210",
                    "40300",
                    "40310",
                    "40400",
                    "40500"
                ]
            }
        ]
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    print("="*60)
    print("EXPORTING TOP PRODUCTS BY REVENUE")
    print("="*60)
    print("Account: 40000 (Sales Revenue)")
    print("Plan Type: FinPlan")
    print("Entity: FCCS_Total Geography")
    print("Scenario: Actual")
    print("Years: FY24")
    print("Period: Dec (YTD)")
    print()
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        print("="*60)
        print("EXPORT RESULT:")
        print("="*60)
        
        if result.get("status") == "success":
            data = result.get("data", {})
            rows = data.get("rows", [])
            
            # Extract revenue values and sort
            products_revenue = []
            for row in rows:
                # Try different ways to get the account name and value
                account_name = row.get("memberName") or row.get("name") or "Unknown"
                row_data = row.get("data", [])
                
                # Get revenue value - could be in different formats
                revenue_value = None
                if row_data and len(row_data) > 0:
                    revenue_value = row_data[0] if isinstance(row_data[0], (int, float)) else None
                elif isinstance(row_data, (int, float)):
                    revenue_value = row_data
                
                if revenue_value and revenue_value != 0:
                    products_revenue.append({
                        "account": account_name,
                        "revenue": revenue_value
                    })
            
            # Sort by revenue descending
            products_revenue.sort(key=lambda x: abs(x["revenue"]) if x["revenue"] else 0, reverse=True)
            
            # Display top 10
            print("\nTOP 10 PRODUCTS BY REVENUE:")
            print("-" * 60)
            for i, product in enumerate(products_revenue[:10], 1):
                revenue = product["revenue"]
                revenue_str = f"${revenue:,.2f}" if isinstance(revenue, (int, float)) else str(revenue)
                print(f"{i:2}. {product['account']:30} {revenue_str:>15}")
            
            # Save full result
            with open("top_products_revenue.json", "w", encoding="utf-8") as f:
                json.dump({
                    "top_10_products": products_revenue[:10],
                    "full_data": result
                }, f, indent=2, ensure_ascii=False)
            print(f"\nFull data saved to: top_products_revenue.json")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return result
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(export_top_products_revenue())
    if result and result.get("status") == "success":
        print("\n[SUCCESS] Export completed successfully!")
    else:
        print("\n[FAILED] Export failed!")

