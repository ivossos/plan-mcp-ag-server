# Dimension Intersections for Rooms.docx Accounts - FCCS Application

## Application: Consol (FCCS)

## Accounts from rooms.docx

1. **Rooms revenue** → Account: `410000`
2. **Fnb revenue** (Food & Beverage) → Account: `420000`
3. **F&B Revenue IRD** (In-Room Dining) → Account: To be identified
4. **F&B Revenue BQT** (Banquet) → Account: `Banquets Catering Revenue`
5. **F&B Revenue Mini Bar** → Accounts: `421800`, `422400`
6. **OPEX - Variable Cost** → Account: To be identified
7. **OPEX - Fixed Cost** → Account: To be identified

## FCCS Dimension Intersections Structure

FCCS applications use a specific dimension order in grid definitions. Based on the application structure, here are the dimension intersections:

### Standard FCCS Dimension Order:

1. **Years** (Time dimension)
2. **Scenario** (Scenario dimension)
3. **View** (View dimension - e.g., FCCS_YTD)
4. **Entity** (Entity dimension)
5. **ICP** (Intercompany Partner dimension)
6. **Data Source** (Data Source dimension)
7. **Movement** (Movement dimension)
8. **Account** (Account dimension)
9. **Period** (Time dimension)
10. **Consolidation** (Consolidation dimension)
11. **Multi-GAAP** (Multi-GAAP dimension)

### Example Grid Definition for FCCS Export:

```json
{
  "suppressMissingBlocks": true,
  "pov": {
    "members": [
      ["FY24"],                    // Years
      ["Actual"],                  // Scenario
      ["FCCS_YTD"],               // View
      ["FCCS_Entity Total"],      // Entity
      ["FCCS_Intercompany Top"],   // ICP
      ["FCCS_Total Data Source"],  // Data Source
      ["FCCS_Mvmts_Total"],       // Movement
      ["FCCS_Total Geography"],    // (Additional Entity level)
      ["Entity Currency"],         // Currency
      ["Total Custom 3"],          // Custom dimension
      ["Total Region"],            // Region
      ["Total Venturi Entity"],    // Custom entity
      ["Total Custom 4"]          // Custom dimension
    ]
  },
  "columns": [
    {
      "members": [["Jan"], ["Feb"], ["Mar"], ["Apr"], ["May"], ["Jun"], 
                  ["Jul"], ["Aug"], ["Sep"], ["Oct"], ["Nov"], ["Dec"]]
    }
  ],
  "rows": [
    {
      "members": [["410000"]]  // Rooms Revenue account
    }
  ]
}
```

## Dimension Intersections for Each Account

### 1. Rooms Revenue (410000)

**POV Members:**
- Years: `FY24` (or specific fiscal year)
- Scenario: `Actual` (or Budget, Forecast)
- View: `FCCS_YTD` (or Period)
- Entity: `FCCS_Entity Total` or `FCCS_Total Geography`
- ICP: `FCCS_Intercompany Top`
- Data Source: `FCCS_Total Data Source`
- Movement: `FCCS_Mvmts_Total`
- Additional: `FCCS_Total Geography`, `Entity Currency`, `Total Custom 3`, `Total Region`, `Total Venturi Entity`, `Total Custom 4`

**Columns:** Periods (Jan through Dec)

**Rows:** Account `410000`

### 2. F&B Revenue (420000)

**Same POV structure as above, but:**
- **Rows:** Account `420000`

### 3. F&B Revenue Mini Bar

**Accounts:** `421800` (Mini Bar Food Revenue) and `422400` (Mini Bar Beverage Revenue)

**Same POV structure, but:**
- **Rows:** Accounts `421800` and/or `422400`

## Notes on rooms.docx

The `rooms.docx` file contains:
- **Text content:** Only account names (no dimension intersection specifications)
- **Images:** 7 images (image1.png through image7.png) - these may contain dimension intersection details

## Recommendation

Since the document only contains account names in text, the dimension intersection specifications might be:
1. **In the images** - The 7 PNG images may contain tables or diagrams showing dimension intersections
2. **Implicit** - Standard FCCS intersections should be used (as shown above)
3. **To be defined** - Dimension intersections need to be specified based on reporting requirements

## Next Steps

1. **Check images** - Extract and analyze the 7 PNG images in the document for dimension intersection details
2. **Use standard intersections** - Apply the standard FCCS dimension intersection structure shown above
3. **Validate members** - Verify all dimension members exist in the FCCS application
4. **Export data** - Use the FCCS export_data_slice function with the correct grid definition format





