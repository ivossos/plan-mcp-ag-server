# Planning Agent Feedback Tools - Setup Complete ✅

## What Was Added

I've added feedback tools to the Planning agent so you can rate tool executions directly in Claude GUI:

1. **`submit_feedback`** - Rate a tool execution (1-5 stars)
2. **`get_recent_executions`** - Find recent executions to rate

## Files Modified

- ✅ Created `planning_agent/tools/feedback.py` - New feedback tools
- ✅ Updated `planning_agent/agent.py` - Registered feedback tools in TOOL_HANDLERS

## How to Use (After Restart)

### Step 1: Restart the MCP Server

The MCP server needs to be restarted to pick up the new tools. Restart your MCP server/Claude Desktop.

### Step 2: Rate Tool Executions

After any tool execution, you'll see an `execution_id` in the result. You can then rate it:

**Example:**
```
You: "Get dimensions for the application"
Claude: [Executes get_dimensions]
        Result: {
          "status": "success",
          "data": {...},
          "execution_id": 123  ← Use this ID!
        }

You: "Rate that 5 stars, it worked perfectly"
Claude: [Calls submit_feedback]
        {
          "execution_id": 123,
          "rating": 5,
          "feedback": "Perfect results!"
        }
```

### Step 3: Find Executions to Rate

If you want to rate previous executions:

```
You: "Show me recent tool executions I can rate"
Claude: [Calls get_recent_executions]
        Shows list of recent executions with IDs
```

## Rating Scale

- **5 stars**: Excellent - Tool worked perfectly
- **4 stars**: Good - Tool worked well
- **3 stars**: Average - Tool worked but could be better
- **2 stars**: Poor - Tool had issues
- **1 star**: Bad - Tool failed

## Benefits

✅ **Improves RL Learning** - System learns which tools work best for you
✅ **Real-time Feedback** - Rate immediately after execution
✅ **Easy to Use** - Just use the execution_id from any tool result
✅ **Works in Claude GUI** - No need for external tools or APIs

## Next Steps

1. **Restart your MCP server** to load the new tools
2. **Execute a tool** (e.g., `get_dimensions`)
3. **Rate it** using `submit_feedback` with the execution_id
4. **Check recent executions** using `get_recent_executions` to find more to rate

The feedback will help the RL system learn and improve tool selection for future requests!





