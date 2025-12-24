# Rooms Accounts Data Retrieval Summary

## Accounts Identified from rooms.docx

### Successfully Mapped Accounts:

1. **Rooms Revenue**
   - Account Code: `410000`
   - Account Name: `410000-Revenue - Rooms Revenue`
   - Type: Dynamic Calc
   - Status: ✅ Account found and verified

2. **F&B Revenue**
   - Account Code: `420000`
   - Account Name: `420000-Revenue - F&B Revenue`
   - Type: Dynamic Calc
   - Status: ✅ Account found and verified

3. **F&B Revenue Mini Bar**
   - Account Codes: 
     - `421800` - Mini Bar Food Revenue (Dynamic Calc)
     - `421810` - Mini Bar Revenue - Food (Store Data)
     - `422400` - Mini Bar Beverage Revenue (Dynamic Calc)
     - `422410` - Mini Bar Revenue - Beverage (Store Data)
   - Status: ✅ Accounts found and verified

4. **F&B Revenue BQT (Banquet)**
   - Account Name: `Banquets Catering Revenue`
   - Status: ✅ Account found (custom named account)

### Accounts Requiring Further Investigation:

5. **F&B Revenue IRD (In-Room Dining)**
   - Related Accounts Found:
     - `439230` - In-Room Items
     - `439240` - In-Room Movies
   - Status: ⚠️ No direct IRD revenue account found - may be under F&B Food/Beverage hierarchy

6. **OPEX - Variable Cost**
   - Status: ⚠️ Not found as direct account - may be tracked via attributes or aggregation

7. **OPEX - Fixed Cost**
   - Status: ⚠️ Not found as direct account - may be tracked via attributes or aggregation

## Data Retrieval Attempts

### API Status:
- ✅ Successfully connected to Planning/FCCS application
- ✅ Application: `Consol` (FCCS type)
- ✅ Dimensions retrieved successfully
- ⚠️ Data export attempts returned 400 Bad Request errors

### Possible Reasons for Data Export Issues:
1. **Account Codes**: The account codes (`410000`, `420000`, etc.) may need to be validated against the actual application
2. **Grid Definition Format**: The grid definition structure may need adjustment for FCCS API
3. **Data Availability**: The accounts may not have data loaded for the requested periods/scenarios
4. **API Permissions**: May require specific permissions or authentication configuration
5. **Plan Type**: May need to use correct plan type name (currently using "Consol")

## Recommended Next Steps:

1. **Validate Account Codes**: Verify that accounts `410000`, `420000`, `421800`, `422400` exist in the actual FCCS application
2. **Check Available Data**: Verify which periods, years, and scenarios have data loaded
3. **Review API Documentation**: Check FCCS REST API documentation for correct grid definition format
4. **Test with Known Accounts**: Try retrieving data for accounts known to have data
5. **Use Web Interface**: Consider using the FCCS web interface to verify account existence and data availability

## Dimension Intersections Required:

For each account, the following dimensions need to be specified:
- **Account**: [Account code/name]
- **Entity**: [Entity member - e.g., "FCCS_Total Geography"]
- **Period**: [Time period - e.g., "Jan", "Feb", etc.]
- **Years**: [Fiscal year - e.g., "FY24", "FY25"]
- **Scenario**: [Scenario type - e.g., "Actual", "Budget", "Forecast"]
- **View**: [View type - e.g., "YTD", "Period"]
- **ICP**: [Intercompany Partner - typically "FCCS_Intercompany Top" or "None"]
- **Data Source**: [Data source - typically "FCCS_Total Data Source"]
- **Movement**: [Movement type - typically "FCCS_Mvmts_Total"]
- **Multi-GAAP**: [GAAP type if applicable]
- **Consolidation**: [Consolidation method if applicable]

## Example Grid Definition (FCCS Format):

```json
{
  "suppressMissingBlocks": true,
  "pov": {
    "members": [
      ["FY24"],
      ["Actual"],
      ["FCCS_YTD"],
      ["FCCS_Entity Total"],
      ["FCCS_Intercompany Top"],
      ["FCCS_Total Data Source"],
      ["FCCS_Mvmts_Total"],
      ["FCCS_Total Geography"],
      ["Entity Currency"],
      ["Total Custom 3"],
      ["Total Region"],
      ["Total Venturi Entity"],
      ["Total Custom 4"]
    ]
  },
  "columns": [
    {
      "members": [["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
    }
  ],
  "rows": [
    {
      "members": [["410000"]]
    }
  ]
}
```

## Notes:

- The application is accessible via Planning REST API but is actually an FCCS application
- Account metadata was successfully retrieved from exported CSV files
- Direct API data retrieval requires further configuration or validation
- Consider using the FCCS web interface or EPM Automate for data export if API issues persist





