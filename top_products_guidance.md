# Top 10 Products by Revenue - Guidance

## Current Status

I've connected to the Planning agent successfully. The application is:
- **Application Name**: PlanApp (displayed as "Consol" in some contexts)
- **Application Type**: FCCS (Financial Consolidation and Close)
- **Plan Type**: FinPlan

## Understanding "Products" in This System

In this FCCS application, "products" are likely represented as:

1. **Revenue Accounts** - Different revenue account codes (like 410000 for Rooms Revenue, 420000 for F&B Revenue, etc.)
2. **Entities** - Different business segments or locations (Industrial Segment, Energy Segment, Fire Protection Segment, etc.)
3. **Account Sub-accounts** - Child accounts under main revenue accounts

## Available Revenue Accounts

Based on the Account dimension, here are key revenue accounts:

- **FCCS_Sales** - Main Sales/Revenue account
- **40000** - Sales account code
- **40100-40106** - Various sales sub-accounts
- **40200, 40210** - Additional sales accounts
- **40300, 40310** - More sales accounts
- **40400, 40500** - Additional revenue accounts
- **410000** - Rooms Revenue (hotel-specific)
- **420000** - F&B Revenue (Food & Beverage)

## How to Get Top 10 Products by Revenue

### Option 1: Query by Revenue Accounts

Export revenue data broken down by different revenue account codes. The accounts with the highest revenue values would represent the "top products."

### Option 2: Query by Entities/Segments

Export revenue data broken down by entities (segments like Industrial, Energy, Fire Protection). Each segment might represent different product lines.

### Option 3: Use Account Hierarchy

Query the Sales account (FCCS_Sales or 40000) and expand to see child accounts, which might represent different products.

## Recommended Query Structure

```python
grid_definition = {
    "pov": {
        "members": [
            ["FCCS_Sales"],              # or ["40000"]
            ["FCCS_Total Geography"],
            ["Actual"],
            ["FY24"],                    # or current fiscal year
            ["Dec"],
            ["YTD"],
            ["None"],
            ["None"],
            ["None"],
            ["None"],
            ["None"]
        ]
    },
    "columns": [{"dimension": "Period", "members": ["Dec"]}],
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
```

## Next Steps

1. Verify the correct account codes that represent different products
2. Ensure the grid definition format matches your Planning application's requirements
3. Export the data and sort by revenue value to get the top 10
4. Consider querying by entities if products are tracked at the entity level

## Note

The export_data_slice function is currently returning 400 Bad Request errors. This might be due to:
- Incorrect grid definition format for this specific application
- Missing or incorrect dimension members
- Application-specific requirements not met

You may need to work with your Planning administrator to:
- Verify the correct plan type name
- Confirm the exact dimension member names
- Get the correct grid definition format for your application

