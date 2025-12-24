# export_data_slice Usage Guide

## Function Signature

```python
async def export_data_slice(
    plan_type: str,
    grid_definition: dict[str, Any]
) -> dict[str, Any]
```

## Parameters

- **plan_type**: The name of the plan type (e.g., 'FinPlan', 'FinRPT')
- **grid_definition**: The data grid definition with pov, columns, and rows

## Return Format

```python
{
    "status": "success",
    "data": {
        "rows": [
            {
                "memberName": "410000",
                "data": [12345.67, 23456.78, ...]  # Values for each column
            },
            ...
        ],
        "columns": [...]
    }
}
```

## Grid Definition Format (Planning - NOT FCCS)

### Basic Structure

```python
grid_definition = {
    "suppressMissingBlocks": True,
    "pov": {
        "members": [
            ["Account"],      # Account dimension
            ["Total Entity"], # Entity dimension
            ["Actual"],       # Scenario dimension
            ["FY25"],         # Years dimension
            ["Dec"]           # Period dimension
            # Note: Only 5 dimensions in POV for Planning format
        ]
    },
    "columns": {
        "members": [["Dec"]]  # Single period
    },
    "rows": {
        "members": [["410000"]]  # Single account
    }
}
```

### Multiple Accounts in Rows

```python
grid_definition = {
    "suppressMissingBlocks": True,
    "pov": {
        "members": [
            ["400000"],       # Account: Revenue parent
            ["Total Entity"], # Entity
            ["Actual"],       # Scenario
            ["FY25"],         # Years
            ["Dec"]           # Period
        ]
    },
    "columns": {
        "members": [["Dec"]]
    },
    "rows": {
        "members": [
            ["400000"],  # Each account wrapped in its own array
            ["410000"],
            ["420000"],
            ["411000"],
            ["412000"]
        ]
    }
}
```

## Usage Example

```python
from planning_agent.agent import initialize_agent, execute_tool

async def get_revenue_data():
    await initialize_agent()
    
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                ["400000"],
                ["Total Entity"],
                ["Actual"],
                ["FY25"],
                ["Dec"]
            ]
        },
        "columns": {
            "members": [["Dec"]]
        },
        "rows": {
            "members": [
                ["400000"],
                ["410000"],
                ["420000"]
            ]
        }
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    result = await execute_tool("export_data_slice", arguments)
    
    if result.get("status") == "success":
        data = result.get("data", {})
        rows = data.get("rows", [])
        
        for row in rows:
            account = row.get("memberName")
            revenue_values = row.get("data", [])
            print(f"{account}: {revenue_values}")
    else:
        print(f"Error: {result.get('error')}")
```

## Important Notes

1. **Planning Format (NOT FCCS)**: Use only 5 dimensions in POV: Account, Entity, Scenario, Years, Period
2. **Rows Format**: Each member must be wrapped in its own array: `[["account1"], ["account2"]]`
3. **Columns Format**: Use object with members: `{"members": [["Dec"]]}`
4. **POV Format**: Use object with members array: `{"members": [["Account"], ["Entity"], ...]}`
5. **Local CSV Files**: Always check `ExportedMetadata_*.csv` files in root folder for valid dimension members

## Common Errors

- **400 Bad Request**: Usually means grid definition format is incorrect or dimension members don't exist
- **Check CSV files**: Verify account/entity names exist in `ExportedMetadata_Account.csv` and `ExportedMetadata_Entity.csv`
- **Dimension Order**: Must match Planning application's dimension order (Account, Entity, Scenario, Years, Period)

