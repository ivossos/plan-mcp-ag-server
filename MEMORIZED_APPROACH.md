# Memorized Approach for Planning Agent

## Key Rules

### 0. CRITICAL: Never Connect to FCCS from Plan Agent
- **NEVER use Planning Agent to connect to FCCS applications**
- Planning Agent is ONLY for Oracle Planning applications
- For FCCS applications (like "Consol"), use the **FCCS Agent** instead (`mcp_fccs-agent_*` tools)
- If `appType` is "FCCS" or application name contains "Consol"/"FCCS"/"Consolidation" → Use FCCS Agent, NOT Planning Agent

### 1. NEVER Use FCCS Export Data Format
- **When using Planning agent, NEVER use FCCS export data format**
- Planning applications use different dimension structure than FCCS
- Planning format dimensions: Account, Entity, Scenario, Years, Period, Version, Currency, Future1, CostCenter, Region
- FCCS format includes: View, ICP, Data Source, Movement, Multi-GAAP, Consolidation (DO NOT USE THESE)

### 2. Always Check Local CSV Files for Dimensions and Hierarchies
- **Location**: Root project folder
- **Files**: `ExportedMetadata_<DimensionName>.csv`
- **Available files**:
  - `ExportedMetadata_Account.csv` - Account dimension with parent-child hierarchies
  - `ExportedMetadata_Entity.csv` - Entity dimension
  - `ExportedMetadata_CostCenter.csv` - CostCenter dimension
  - `ExportedMetadata_Region.csv` - Region dimension
  - `ExportedMetadata_Scenario.csv` - Scenario dimension
  - `ExportedMetadata_Currency.csv` - Currency dimension
  - `ExportedMetadata_Version.csv` - Version dimension
  - `ExportedMetadata_Future1.csv` - Future1 dimension

### 3. CSV File Structure
- First column: Member name (e.g., "Account", "Entity")
- Second column: Parent (shows hierarchy relationships)
- Other columns: Metadata (Alias, Description, Account Type, etc.)

### 4. Revenue Account Hierarchy (from CSV)
```
400000 - Revenue (parent)
├── 410000 - Rooms Revenue
│   ├── 411000 - Transient Rooms Revenue
│   ├── 412000 - Group Rooms Revenue
│   ├── 413000 - Contract Rooms Revenue
│   ├── 414000 - Other Rooms Revenue
│   └── 419000 - Rooms: Allowances
├── 420000 - F&B Revenue
│   ├── 421000 - F&B Revenue - Food
│   ├── 422000 - F&B Revenue - Beverage
│   ├── 423000 - F&B Revenue - Other
│   └── 429000 - F&B Revenue: Allowances
├── 430000 - Other Operated Revenue
└── 440000 - Miscellaneous Income
```

### 5. How to Use CSV Files
- Read CSV files to get dimension members and their hierarchies
- Use parent-child relationships to understand account/product structure
- Filter accounts by keywords (revenue, sales, income) or account codes (starting with 4 for revenue)
- Use these accounts in grid definitions for data export

### 6. Planning Grid Definition Format
```python
grid_definition = {
    "suppressMissingBlocks": True,
    "pov": {
        "members": [
            ["Account"],      # Account dimension
            ["Total Entity"], # Entity dimension
            ["Actual"],       # Scenario dimension
            ["FY25"],         # Years dimension
            ["Dec"],          # Period dimension
            ["Working"],      # Version dimension
            ["USD"],         # Currency dimension
            ["No Future1"],   # Future1 dimension
            ["Total CostCenter"], # CostCenter dimension
            ["Total Region"]     # Region dimension
        ]
    },
    "columns": [{"members": [["Dec"]]}],
    "rows": [
        {
            "dimension": "Account",
            "members": ["400000", "410000", "420000"]
        }
    ]
}
```

## Summary
1. ✅ Use Planning format (NOT FCCS format)
2. ✅ Check local CSV files in root project folder for dimensions/hierarchies
3. ✅ Use CSV parent-child relationships to understand structure
4. ✅ Filter accounts/products from CSV data
5. ✅ Use correct dimension order in grid definitions

