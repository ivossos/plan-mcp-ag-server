# Dimension Intersections for Rooms.docx Accounts

## Accounts from rooms.docx

1. **Rooms revenue** → Account: `410000`
2. **Fnb revenue** (Food & Beverage) → Account: `420000`
3. **F&B Revenue IRD** (In-Room Dining) → Account: To be identified
4. **F&B Revenue BQT** (Banquet) → Account: `Banquets Catering Revenue`
5. **F&B Revenue Mini Bar** → Accounts: `421800`, `422400`
6. **OPEX - Variable Cost** → Account: To be identified
7. **OPEX - Fixed Cost** → Account: To be identified

## Standard Dimension Intersections

For each account, the following dimension intersections are typically required:

### Required Dimensions (FCCS/Planning Application):

1. **Account** - The account code/name
2. **Entity** - Organization/entity (e.g., "FCCS_Total Geography" for total, or specific entity)
3. **Period** - Time period (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)
4. **Years** - Fiscal year (e.g., FY24, FY25)
5. **Scenario** - Scenario type (Actual, Budget, Forecast, etc.)
6. **View** - View type (YTD, Period, etc.)
7. **ICP** - Intercompany Partner (typically "None" or "FCCS_Intercompany Top")
8. **Data Source** - Data source (typically "None" or "FCCS_Total Data Source")
9. **Movement** - Movement type (typically "None" or "FCCS_Mvmts_Total")
10. **Multi-GAAP** - GAAP type (typically "None")
11. **Consolidation** - Consolidation method (typically "None")

## Example Dimension Intersections

### For Rooms Revenue (410000):

**POV (Point of View):**
- Account: `410000`
- Entity: `FCCS_Total Geography` (or specific entity)
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

**Rows:** Account (410000)

### For F&B Revenue (420000):

**POV:**
- Account: `420000`
- Entity: `FCCS_Total Geography`
- Scenario: `Actual`
- Years: `FY24`
- Period: `Jan`
- View: `YTD`
- ICP: `None`
- Data Source: `None`
- Movement: `None`
- Multi-GAAP: `None`
- Consolidation: `None`

### For F&B Revenue Mini Bar:

**Accounts:** `421800` (Mini Bar Food Revenue) and `422400` (Mini Bar Beverage Revenue)

**POV (same for both):**
- Account: `421800` or `422400`
- Entity: `FCCS_Total Geography`
- Scenario: `Actual`
- Years: `FY24`
- Period: `Jan`
- View: `YTD`
- ICP: `None`
- Data Source: `None`
- Movement: `None`
- Multi-GAAP: `None`
- Consolidation: `None`

## Grid Definition Format for Planning REST API

Based on Planning REST API v3, the grid definition should follow this structure:

```json
{
  "pov": {
    "members": [
      ["Account_Member"],
      ["Entity_Member"],
      ["Scenario_Member"],
      ["Years_Member"],
      ["Period_Member"],
      ["View_Member"],
      ["ICP_Member"],
      ["Data_Source_Member"],
      ["Movement_Member"],
      ["Multi_GAAP_Member"],
      ["Consolidation_Member"]
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

## Dimension Member Validation

Before using these intersections, verify that the following members exist in the application:

- **Entity:** `FCCS_Total Geography` (or specific entities)
- **Scenario:** `Actual`, `Budget`, `Forecast` (verify available scenarios)
- **Years:** `FY24`, `FY25` (verify available fiscal years)
- **Period:** `Jan`, `Feb`, `Mar`, etc. (verify period names)
- **View:** `YTD`, `Period` (verify available views)

## Notes

- The `rooms.docx` file only contains account names, not dimension intersection specifications
- Dimension intersections need to be defined based on the specific reporting requirements
- Default intersections shown above use common FCCS/Planning dimension members
- Actual dimension members may vary based on application configuration
- Some accounts (IRD, OPEX Variable/Fixed Cost) still need to be identified

## Next Steps

1. Validate all dimension member names exist in the Planning application
2. Identify missing accounts (IRD, OPEX Variable/Fixed Cost)
3. Define specific dimension intersections based on reporting needs
4. Test grid definitions with the Planning REST API
5. Export data using validated dimension intersections





