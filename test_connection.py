"""Test connection to Planning agent."""

import asyncio
import sys
import json
from planning_agent.agent import initialize_agent, execute_tool, close_agent

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


async def test_connection():
    """Test the Planning agent connection."""
    print("Initializing Planning agent...")
    app_name = await initialize_agent()
    print(f"[OK] Connected to: {app_name}\n")
    
    print("Testing get_application_info tool...")
    result = await execute_tool("get_application_info", {})
    print("[OK] Application Info:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\nTesting get_dimensions tool...")
    result = await execute_tool("get_dimensions", {})
    print(f"[OK] Dimensions retrieved: {len(result.get('items', []))} dimensions")
    
    await close_agent()
    print("\n[OK] Connection test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_connection())

