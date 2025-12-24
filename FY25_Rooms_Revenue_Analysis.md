# FY25 Rooms Revenue Analysis

**Generated:** December 23, 2025  
**Entity:** E501 (L7 Chicago)  
**Cost Center:** CC1000 (Rooms Department)  
**Region:** R131 (Illinois)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **FY25 Forecast (Full Year)** | $130,728,750 |
| **FY25 Actuals YTD (Jan-May)** | $3,831,043 |
| **Annualized Run Rate** | ~$9.2M |
| **Forecast Gap** | Significant disconnect identified |

---

## Monthly Breakdown - Forecast vs Actuals

| Month | Actual | Forecast | Variance | Var % |
|-------|-------:|--------:|---------:|------:|
| Jan | $305,415 | $100,881,125 | $(100,575,710) | -99.7% |
| Feb | $382,188 | $10,881,125 | $(10,498,937) | -96.5% |
| Mar | $822,563 | $10,881,125 | $(10,058,562) | -92.4% |
| Apr | $915,046 | $898,375 | $16,671 | +1.9% |
| May | $1,405,831 | $898,375 | $507,456 | +56.5% |
| Jun | — | $898,375 | — | — |
| Jul | — | $898,375 | — | — |
| Aug | — | $898,375 | — | — |
| Sep | — | $898,375 | — | — |
| Oct | — | $898,375 | — | — |
| Nov | — | $898,375 | — | — |
| Dec | — | $898,375 | — | — |
| **YTD (Jan-May)** | **$3,831,043** | **$124,440,125** | — | — |
| **Full Year** | — | **$130,728,750** | — | — |

---

## Revenue by Type (Account 410000 Children)

### FY25 Forecast - Full Year

| Account | Description | Amount | % of Total |
|---------|-------------|-------:|:----------:|
| 411000 | Transient Rooms Revenue | $127,908,750 | 97.8% |
| 412000 | Group Rooms Revenue | $2,820,000 | 2.2% |
| 413000 | Contract Rooms Revenue | — | — |
| 414000 | Other Rooms Revenue | — | — |
| **410000** | **Total Rooms Revenue** | **$130,728,750** | **100%** |

### FY25 Actuals - YTD (Jan-May)

| Account | Description | Amount | % of Total |
|---------|-------------|-------:|:----------:|
| 411000 | Transient Rooms Revenue | $3,200,990 | 83.5% |
| 412000 | Group Rooms Revenue | $573,008 | 15.0% |
| 413000 | Contract Rooms Revenue | — | — |
| 414000 | Other Rooms Revenue | $57,969 | 1.5% |
| **410000** | **Total Rooms Revenue** | **$3,831,967** | **100%** |

---

## Key Findings

### 1. Forecast Data Quality Issue
- **Jan-Mar forecasts are significantly inflated** - possibly containing BegBal, seed data, or prior year carryover
- January alone shows $100.9M (77% of annual forecast) which is unrealistic for a single month

### 2. Apr-May Trending Better
- April actuals ($915K) closely matched forecast ($898K) - variance of +1.9%
- May actuals ($1.4M) outperformed forecast by 56.5%

### 3. Revenue Mix Difference
- **Forecast assumes 98% Transient** revenue
- **Actuals show more balanced mix**: 84% Transient, 15% Group, 1.5% Other

### 4. Annualized Projection
- YTD run rate suggests ~$9.2M annual revenue vs $130.7M forecast
- This represents a **93% gap** between forecast and projected actuals

---

## Recommendations

1. **Review Jan-Mar forecast entries** - Clean up any BegBal or seed data contamination
2. **Reforecast based on YTD trends** - Use Apr-May actuals as baseline for remaining months
3. **Adjust revenue mix assumptions** - Group revenue is outperforming relative expectations
4. **Investigate May spike** - Understand drivers of 56% outperformance

---

## Technical Details

**POV Used:**
- Years: FY25
- Scenario: Forecast / Actual
- Version: Final
- Currency: USD
- Entity: E501
- CostCenter: CC1000
- Future1: No Future1
- Region: R131

**Data Source:** Oracle EPBCS (PlanApp) via REST API
