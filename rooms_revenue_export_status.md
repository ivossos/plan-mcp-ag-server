# Rooms Revenue Export Status

## Account Information
- **Account Code:** `410000`
- **Account Name:** `410000-Revenue - Rooms Revenue`
- **Account Type:** Dynamic Calc
- **Status:** ✅ Account verified and exists in Planning application
- **Plan Types:** Used in `FinPlan` and `FinRPT`

## Export Attempts

### Attempt 1: Complex Grid Definition
- **Format:** Full grid definition with suppressMissingBlocks, nested members structure
- **Result:** 400 Bad Request
- **Error:** API rejected the grid definition format

### Attempt 2: Simplified Grid Definition  
- **Format:** Simplified pov, columns, rows arrays
- **Result:** 400 Bad Request
- **Error:** API still rejected the format

## Possible Issues

1. **Grid Definition Format:** The Planning REST API may require a specific grid definition structure that differs from what we've tried
2. **Dimension Order:** The POV members may need to be in a specific order matching the application's dimension order
3. **Member Names:** Some member names (like "FCCS_Total Geography", "YTD", "FY24") may need to be validated or may not exist in this application
4. **Plan Type:** "FinPlan" may not be the correct plan type name - might need to verify available plan types
5. **API Version:** The REST API version or endpoint structure may require different parameters

## Next Steps

1. **Verify Plan Types:** Check what plan types are actually available in the application
2. **Check Dimension Members:** Validate that all dimension members exist:
   - Entity: "FCCS_Total Geography"
   - Scenario: "Actual"  
   - Years: "FY24"
   - Period: "Jan", "Feb", etc.
   - View: "YTD"
3. **Review API Documentation:** Check Oracle Planning REST API v3 documentation for correct grid definition format
4. **Test with Web Interface:** Use Planning web interface to export data and compare the grid definition format
5. **Try Different Format:** Experiment with alternative grid definition structures

## Account Hierarchy Confirmed

The Rooms Revenue account (410000) has the following child accounts:
- 411000 - Revenue - Transient Rooms Revenue
- 412000 - Revenue - Group Rooms Revenue  
- 413000 - Revenue - Contract Rooms Revenue
- 414000 - Revenue - Other Rooms Revenue
- 419000 - Revenue - Rooms: Allowances

All accounts are valid and accessible via the Planning API.

## Recommendation

The account exists and is accessible, but data export requires the correct grid definition format. Consider:
1. Using the Planning web interface to export data and inspect the grid definition format
2. Reviewing Oracle Planning REST API documentation
3. Testing with a known working grid definition from another export
4. Verifying all dimension member names match exactly what's in the application





