"""Test revenue export with working format, then expand to get top products."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def test_and_export():
    await initialize_agent()
    
    # First test: Use the exact working format with Rooms Revenue
    print("="*60)
    print("TEST 1: Rooms Revenue (410000) - Verify format works")
    print("="*60)
    
    grid_definition_1 = {
        "pov": {
            "members": [
                ["410000"],                    # Account: Rooms Revenue
                ["FCCS_Total Geography"],      # Entity: Total Geography
                ["Actual"],                    # Scenario: Actual
                ["FY24"],                      # Years: Fiscal Year 2024
                ["Dec"],                       # Period: December
                ["YTD"],                       # View: Year-to-Date
                ["None"],                      # ICP: None
                ["None"],                      # Data Source: None
                ["None"],                      # Movement: None
                ["None"],                      # Multi-GAAP: None
                ["None"]                       # Consolidation: None
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
                "members": ["410000", "420000", "40000"]  # Try multiple revenue accounts
            }
        ]
    }
    
    arguments_1 = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition_1
    }
    
    try:
        result_1 = await execute_tool("export_data_slice", arguments_1)
        print("Result:", json.dumps(result_1, indent=2, ensure_ascii=False))
        
        if result_1.get("status") == "success":
            data = result_1.get("data", {})
            rows = data.get("rows", [])
            
            print("\n" + "="*60)
            print("TOP REVENUE ACCOUNTS (Products):")
            print("="*60)
            
            products = []
            for row in rows:
                account = row.get("memberName") or row.get("name") or "Unknown"
                row_data = row.get("data", [])
                revenue = row_data[0] if row_data and len(row_data) > 0 else 0
                
                if revenue and revenue != 0:
                    products.append({"account": account, "revenue": revenue})
            
            products.sort(key=lambda x: abs(x["revenue"]) if x["revenue"] else 0, reverse=True)
            
            for i, p in enumerate(products[:10], 1):
                rev = p["revenue"]
                rev_str = f"${rev:,.2f}" if isinstance(rev, (int, float)) else str(rev)
                print(f"{i:2}. {p['account']:30} {rev_str:>15}")
            
            return result_1
        else:
            print(f"Error: {result_1.get('error')}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_and_export())

