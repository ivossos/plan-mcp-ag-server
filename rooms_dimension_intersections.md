# Dimension Intersections for Rooms.docx Accounts

## Summary
This document maps the accounts listed in `rooms.docx` to their corresponding account codes in the Planning application and identifies the required dimension intersections.

## Accounts from rooms.docx

### 1. Rooms Revenue
- **Account Code:** `410000`
- **Account Name:** `410000-Revenue - Rooms Revenue`
- **Account Type:** Dynamic Calc (aggregates all room revenue sub-accounts)
- **Parent Account:** `400000` (Revenue)
- **Dimension Intersections Required:**
  - Account: `410000`
  - Entity: [Any Entity from Entity dimension]
  - Period: [Any Period from Period dimension]
  - Scenario: [Any Scenario from Scenario dimension]
  - Years: [Any Year from Years dimension]
  - View: [Any View from View dimension]
  - Other dimensions as applicable (ICP, Data Source, Movement, Multi-GAAP, Consolidation)

### 2. F&B Revenue (Food & Beverage Revenue)
- **Account Code:** `420000`
- **Account Name:** `420000-Revenue - F&B Revenue`
- **Account Type:** Dynamic Calc
- **Parent Account:** `400000` (Revenue)
- **Dimension Intersections Required:**
  - Account: `420000`
  - Entity: [Any Entity]
  - Period: [Any Period]
  - Scenario: [Any Scenario]
  - Years: [Any Year]
  - View: [Any View]

### 3. F&B Revenue IRD (In-Room Dining)
- **Note:** No direct "In-Room Dining Revenue" account found in main F&B hierarchy
- **Related Accounts Found:**
  - `439230` - In-Room Items (under Other Minor Operated Dept. Revenue)
  - `439240` - In-Room Movies (under Other Minor Operated Dept. Revenue)
  - `102210IRD` - COS In-Room Dining (Cost of Sales account)
- **Possible Account:** May be under `421000` (F&B Revenue - Food) or `422000` (F&B Revenue - Beverage)
- **Dimension Intersections Required:**
  - Account: [To be confirmed - may need to search for IRD-specific account]
  - Entity: [Any Entity]
  - Period: [Any Period]
  - Scenario: [Any Scenario]
  - Years: [Any Year]
  - View: [Any View]

### 4. F&B Revenue BQT (Banquet)
- **Account Code:** `Banquets Catering Revenue` (found as a named account)
- **Related Accounts:**
  - Multiple child accounts under "Banquets Catering Revenue" (41790903, 41790904, etc.)
- **Note:** This appears to be a custom account name, not a standard numbered account
- **Dimension Intersections Required:**
  - Account: `Banquets Catering Revenue`
  - Entity: [Any Entity]
  - Period: [Any Period]
  - Scenario: [Any Scenario]
  - Years: [Any Year]
  - View: [Any View]

### 5. F&B Revenue Mini Bar
- **Account Codes:**
  - `421800` - Mini Bar Food Revenue (Dynamic Calc)
  - `421810` - Mini Bar Revenue - Food (Store Data)
  - `422400` - Mini Bar Beverage Revenue (Dynamic Calc)
  - `422410` - Mini Bar Revenue - Beverage (Store Data)
- **Parent Accounts:**
  - `421800` under `421000` (F&B Revenue - Food)
  - `422400` under `422000` (F&B Revenue - Beverage)
- **Dimension Intersections Required:**
  - Account: `421800` or `422400` (or child accounts `421810`, `422410`)
  - Entity: [Any Entity]
  - Period: [Any Period]
  - Scenario: [Any Scenario]
  - Years: [Any Year]
  - View: [Any View]

### 6. OPEX - Variable Cost
- **Status:** Not found as a direct account named "Variable Cost"
- **Note:** OPEX (Operating Expenses) accounts typically start with 6xxxx series
- **Found Operating Expenses Account:**
  - `600000` - Payroll & Related Expenses (Dynamic Calc)
  - Parent: "Total Operating Expenses"
- **Possible Accounts:**
  - Variable costs may be categorized under specific expense accounts (60000-69999 series)
  - May need to identify variable vs fixed cost accounts based on account attributes or custom dimensions
  - Could be tracked via a custom dimension or attribute rather than separate accounts
- **Dimension Intersections Required:**
  - Account: [To be identified - may need to aggregate variable cost accounts]
  - Entity: [Any Entity]
  - Period: [Any Period]
  - Scenario: [Any Scenario]
  - Years: [Any Year]
  - View: [Any View]
  - **Note:** May require filtering by account type or custom attribute to identify variable costs

### 7. OPEX - Fixed Cost
- **Status:** Not found as a direct account named "Fixed Cost"
- **Note:** OPEX (Operating Expenses) accounts typically start with 6xxxx series
- **Found Operating Expenses Account:**
  - `600000` - Payroll & Related Expenses (Dynamic Calc)
  - Parent: "Total Operating Expenses"
- **Possible Accounts:**
  - Fixed costs may be categorized under specific expense accounts (60000-69999 series)
  - May need to identify variable vs fixed cost accounts based on account attributes or custom dimensions
  - Could be tracked via a custom dimension or attribute rather than separate accounts
- **Dimension Intersections Required:**
  - Account: [To be identified - may need to aggregate fixed cost accounts]
  - Entity: [Any Entity]
  - Period: [Any Period]
  - Scenario: [Any Scenario]
  - Years: [Any Year]
  - View: [Any View]
  - **Note:** May require filtering by account type or custom attribute to identify fixed costs

## Standard Dimension Intersection Structure

For Oracle Planning/FCCS applications, dimension intersections typically include:

1. **Account** - The account code/name
2. **Entity** - The entity/organization (393 entities found)
3. **Period** - Time period (Month, Quarter, Year, etc.)
4. **Scenario** - Scenario type (Actual, Budget, Forecast, etc.)
5. **Years** - Fiscal year
6. **View** - View type
7. **ICP** - Intercompany Partner (if applicable)
8. **Data Source** - Source of data
9. **Movement** - Movement type (if applicable)
10. **Multi-GAAP** - GAAP type (if applicable)
11. **Consolidation** - Consolidation method (if applicable)

## Example Dimension Intersection Query

To query data for Rooms Revenue:
```
Account: 410000
Entity: [Specific Entity or FCCS_Total Geography]
Period: [Specific Period or All]
Scenario: [Specific Scenario or All]
Years: [Specific Year or All]
View: [Specific View or All]
```

## Next Steps

1. **Confirm IRD Account:** Search for In-Room Dining specific revenue account
2. **Identify OPEX Accounts:** Search for Variable Cost and Fixed Cost accounts in 60000 series
3. **Validate Entity List:** Confirm which entities should be included in intersections
4. **Define Period/Scenario:** Determine which periods and scenarios are relevant
5. **Create Data Grid:** Use `export_data_slice` to retrieve data for these intersections

## Related Account Hierarchies

### Rooms Revenue Hierarchy (410000)
- 411000 - Revenue - Transient Rooms Revenue
- 412000 - Revenue - Group Rooms Revenue
- 413000 - Revenue - Contract Rooms Revenue
- 414000 - Revenue - Other Rooms Revenue
- 419000 - Revenue - Rooms: Allowances

### F&B Revenue Hierarchy (420000)
- 421000 - Revenue - F&B Revenue - Food
- 422000 - Revenue - F&B Revenue - Beverage
- 423000 - Revenue - F&B Revenue - Other

