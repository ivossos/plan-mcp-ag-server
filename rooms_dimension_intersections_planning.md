# Dimension Intersections for Rooms.docx Accounts - Planning Application

## Application: PlanApp (Planning)

## Accounts from rooms.docx

1. **Rooms revenue** → Account: `410000` ✅ Verified
2. **Fnb revenue** (Food & Beverage) → Account: `420000` ✅ Verified  
3. **F&B Revenue IRD** (In-Room Dining) → Account: To be identified
4. **F&B Revenue BQT** (Banquet) → Account: To be identified
5. **F&B Revenue Mini Bar** → Accounts: `421800` (Food), `422400` (Beverage) ✅ Verified
6. **OPEX - Variable Cost** → Account: To be identified
7. **OPEX - Fixed Cost** → Account: To be identified

## Planning Application Dimensions

Based on the Planning application structure, the following dimensions are available:

1. **Account** - Account dimension (verified: 410000 exists)
2. **Entity** - Entity dimension (393 members available, including "FCCS_Total Geography")
3. **Period** - Time period dimension (Jan, Feb, Mar, etc.)
4. **Years** - Fiscal year dimension (FY24, FY25, etc.)
5. **Scenario** - Scenario dimension (Actual, Budget, Forecast, etc.)
6. **View** - View dimension (YTD, Period, etc.)
7. **ICP** - Intercompany Partner dimension
8. **Data Source** - Data Source dimension
9. **Movement** - Movement dimension
10. **Multi-GAAP** - Multi-GAAP dimension
11. **Consolidation** - Consolidation dimension

## Standard Dimension Intersections for Planning

### Grid Definition Format for Planning REST API:

```json
{
  "pov": {
    "members": [
      ["410000"],                    // Account: Rooms Revenue
      ["FCCS_Total Geography"],      // Entity: Total Geography
      ["Actual"],                    // Scenario: Actual
      ["FY24"],                      // Years: Fiscal Year 2024
      ["Jan"],                       // Period: January
      ["YTD"],                       // View: Year-to-Date
      ["None"],                      // ICP: None
      ["None"],                      // Data Source: None
      ["None"],                      // Movement: None
      ["None"],                      // Multi-GAAP: None
      ["None"]                       // Consolidation: None
    ]
  },
  "columns": [
    {
      "dimension": "Period",
      "members": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    }
  ],
  "rows": [
    {
      "dimension": "Account",
      "members": ["410000"]
    }
  ]
}
```

## Dimension Intersections for Each Account

### 1. Rooms Revenue (410000)

**POV (Point of View) Members:**
- Account: `410000`
- Entity: `FCCS_Total Geography` (or specific entity from 393 available)
- Scenario: `Actual` (or Budget, Forecast)
- Years: `FY24` (or FY25, etc.)
- Period: `Jan` (or any period)
- View: `YTD` (or Period)
- ICP: `None`
- Data Source: `None`
- Movement: `None`
- Multi-GAAP: `None`
- Consolidation: `None`

**Columns:** Periods (Jan through Dec)

**Rows:** Account `410000`

### 2. F&B Revenue (420000)

**Same POV structure, but:**
- **Rows:** Account `420000`

### 3. F&B Revenue Mini Bar

**Accounts:** `421800` (Mini Bar Food Revenue) and `422400` (Mini Bar Beverage Revenue)

**Same POV structure, but:**
- **Rows:** Accounts `421800` and/or `422400`

## Available Entity Members

The Planning application has 393 Entity members available, including:
- `FCCS_Total Geography` (recommended for total/consolidated view)
- `FCCS_Global Assumptions`
- Various specific entities (01_001, 01_002, etc.)
- Consolidated entities (Industrial Segment, Energy Segment, etc.)

## Notes on rooms.docx

The `rooms.docx` file contains:
- **Text content:** Only account names (no dimension intersection specifications)
- **Images:** 7 PNG images (image1.png through image7.png) - these may contain dimension intersection details

## Recommendation

Since the document only contains account names in text, the dimension intersection specifications might be:
1. **In the images** - The 7 PNG images may contain tables or diagrams showing dimension intersections
2. **Standard intersections** - Use the standard Planning dimension intersection structure shown above
3. **To be defined** - Dimension intersections need to be specified based on reporting requirements

## Next Steps

1. **Check images** - Extract and analyze the 7 PNG images in the document for dimension intersection details
2. **Use standard intersections** - Apply the standard Planning dimension intersection structure shown above
3. **Validate members** - Verify all dimension members exist in the Planning application
4. **Export data** - Use the Planning export_data_slice function with the correct grid definition format

## Account Hierarchy Confirmed

The Rooms Revenue account (410000) has the following child accounts:
- 411000 - Revenue - Transient Rooms Revenue
- 412000 - Revenue - Group Rooms Revenue
- 413000 - Revenue - Contract Rooms Revenue
- 414000 - Revenue - Other Rooms Revenue
- 419000 - Revenue - Rooms: Allowances

All accounts are valid and accessible via the Planning API.





