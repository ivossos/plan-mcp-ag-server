"""Debug export_data_slice tool to understand why it returns null."""

import asyncio
import json
from planning_agent.agent import initialize_agent, execute_tool

async def debug_export():
    """Debug export_data_slice with detailed logging."""
    print("=" * 80)
    print("DEBUGGING export_data_slice")
    print("=" * 80)
    print()
    
    await initialize_agent()
    print("[OK] Agent initialized")
    print()
    
    # Test 1: Simple query with known good values from export_rooms_fy25.py
    print("Test 1: Using format from export_rooms_fy25.py")
    print("-" * 80)
    
    grid_definition_1 = {
        "suppressMissingBlocks": True,
        "pov": [
            ["410000"],                    # Account: Rooms Revenue
            ["Total Entity"],              # Entity: Use from CSV
            ["Actual"],                    # Scenario
            ["FY25"],                      # Years
            ["Dec"],                       # Period
            ["YTD"]                        # View
        ],
        "columns": [
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        ],
        "rows": [
            ["410000"]
        ]
    }
    
    arguments_1 = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition_1
    }
    
    print(f"Arguments: {json.dumps(arguments_1, indent=2)}")
    print()
    
    try:
        result_1 = await execute_tool("export_data_slice", arguments_1)
        print(f"Result status: {result_1.get('status')}")
        print(f"Result keys: {list(result_1.keys())}")
        
        if result_1.get("status") == "error":
            print(f"ERROR: {result_1.get('error')}")
        else:
            data = result_1.get("data", {})
            print(f"Data keys: {list(data.keys())}")
            print(f"Full result: {json.dumps(result_1, indent=2, ensure_ascii=False)}")
            
            # Check for rows
            rows = data.get("rows", [])
            print(f"\nRows found: {len(rows)}")
            if rows:
                print(f"First row: {rows[0]}")
                if rows[0].get("data"):
                    print(f"First row data: {rows[0]['data']}")
    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 80)
    
    # Test 2: Try with different entity name
    print("Test 2: Trying with 'All Entity'")
    print("-" * 80)
    
    grid_definition_2 = {
        "suppressMissingBlocks": True,
        "pov": [
            ["410000"],
            ["All Entity"],
            ["Actual"],
            ["FY25"],
            ["Dec"],
            ["YTD"]
        ],
        "columns": [
            ["Dec"]  # Just one period for testing
        ],
        "rows": [
            ["410000"]
        ]
    }
    
    arguments_2 = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition_2
    }
    
    try:
        result_2 = await execute_tool("export_data_slice", arguments_2)
        print(f"Result: {json.dumps(result_2, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 80)
    
    # Test 3: Check what the tool definition expects
    print("Test 3: Checking tool handler directly")
    print("-" * 80)
    
    from planning_agent.agent import TOOL_HANDLERS
    handler = TOOL_HANDLERS.get("export_data_slice")
    if handler:
        print(f"Handler found: {handler}")
        import inspect
        sig = inspect.signature(handler)
        print(f"Function signature: {sig}")
    else:
        print("Handler not found!")

if __name__ == "__main__":
    asyncio.run(debug_export())




