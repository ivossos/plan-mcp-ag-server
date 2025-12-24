# Important Rules for Planning Agent

## CRITICAL: Never Connect to FCCS from Plan Agent

**RULE: The Planning Agent should NEVER be used to connect to FCCS applications.**

### Why:
- Planning Agent is designed for **Oracle Planning** applications only
- FCCS (Financial Consolidation and Close) applications require the **FCCS Agent**
- These are separate systems with different APIs and data structures

### What to Do Instead:
- For FCCS applications (like "Consol"): Use the **FCCS Agent** (`mcp_fccs-agent_*` tools)
- For Planning applications: Use the **Planning Agent** (`mcp_planning-agent_*` tools)

### How to Identify:
- If `appType` is "FCCS" → Use FCCS Agent
- If `appType` is "HP" (Hyperion Planning) → Use Planning Agent
- Application names containing "Consol", "FCCS", "Consolidation" → Use FCCS Agent

### Example:
- ❌ **WRONG**: Using `mcp_planning-agent_export_data_slice` for "Consol" FCCS app
- ✅ **CORRECT**: Using `mcp_fccs-agent_export_data_slice` or `mcp_fccs-agent_smart_retrieve` for "Consol" FCCS app

---

## Other Important Rules

### Planning Agent Format
- Planning applications use **10 dimensions**: Account, Entity, Scenario, Years, Period, Version, Currency, Future1, CostCenter, Region
- Never use FCCS-specific dimensions (View, ICP, Data Source, Movement, Multi-GAAP, Consolidation) with Planning Agent

### FCCS Agent Format  
- FCCS applications use **11 dimensions**: Account, Entity, Scenario, Years, Period, View, ICP, Data Source, Movement, Multi-GAAP, Consolidation
- Use `smart_retrieve` for simplified queries, or `export_data_slice` with proper FCCS grid definition


