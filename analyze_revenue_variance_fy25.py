"""Analyze Revenue Variance Drivers for FY25 using dimensions from local CSV files."""

import asyncio
import csv
import json
from pathlib import Path
from typing import Optional, List
from planning_agent.agent import initialize_agent, execute_tool

# Load dimensions from local CSV files
def load_scenarios_from_csv() -> List[str]:
    """Load scenario names from ExportedMetadata_Scenario.csv"""
    csv_file = Path("ExportedMetadata_Scenario.csv")
    scenarios = []
    if csv_file.exists():
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                scenario = row.get("Scenario", "").strip()
                if scenario and scenario != "Scenario":  # Skip header
                    scenarios.append(scenario)
    return scenarios if scenarios else ["Actual", "Budget", "Forecast"]

def load_currencies_from_csv() -> List[str]:
    """Load currency names from ExportedMetadata_Currency.csv"""
    csv_file = Path("ExportedMetadata_Currency.csv")
    currencies = []
    if csv_file.exists():
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
        for encoding in encodings:
            try:
                with open(csv_file, "r", encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    fieldnames = reader.fieldnames
                    if fieldnames:
                        currency_col = fieldnames[0]  # First column
                        for row in reader:
                            currency = row.get(currency_col, "").strip()
                            if currency and currency != currency_col:
                                currencies.append(currency)
                    break
            except Exception:
                if encoding == encodings[-1]:
                    raise
                continue
    return currencies if currencies else ["USD"]

def load_costcenters_from_csv() -> List[str]:
    """Load CostCenter members from ExportedMetadata_CostCenter.csv"""
    csv_file = Path("ExportedMetadata_CostCenter.csv")
    costcenters = []
    if csv_file.exists():
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
        for encoding in encodings:
            try:
                with open(csv_file, "r", encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    fieldnames = reader.fieldnames
                    if fieldnames:
                        cc_col = fieldnames[0]
                        for row in reader:
                            cc = row.get(cc_col, "").strip()
                            if cc and cc != cc_col:
                                costcenters.append(cc)
                    break
            except Exception:
                if encoding == encodings[-1]:
                    raise
                continue
    return costcenters if costcenters else ["No CostCenter"]

def load_versions_from_csv() -> List[str]:
    """Load Version members from ExportedMetadata_Version.csv"""
    csv_file = Path("ExportedMetadata_Version.csv")
    versions = []
    if csv_file.exists():
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
        for encoding in encodings:
            try:
                with open(csv_file, "r", encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    fieldnames = reader.fieldnames
                    if fieldnames:
                        version_col = fieldnames[0]
                        for row in reader:
                            version = row.get(version_col, "").strip()
                            if version and version != version_col:
                                versions.append(version)
                    break
            except Exception:
                if encoding == encodings[-1]:
                    raise
                continue
    return versions if versions else ["Working"]

def load_regions_from_csv() -> List[str]:
    """Load Region members from ExportedMetadata_Region.csv"""
    csv_file = Path("ExportedMetadata_Region.csv")
    regions = []
    if csv_file.exists():
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
        for encoding in encodings:
            try:
                with open(csv_file, "r", encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    fieldnames = reader.fieldnames
                    if fieldnames:
                        region_col = fieldnames[0]
                        for row in reader:
                            region = row.get(region_col, "").strip()
                            if region and region != region_col:
                                regions.append(region)
                    break
            except Exception:
                if encoding == encodings[-1]:
                    raise
                continue
    return regions if regions else ["No Region"]

def load_future1_from_csv() -> List[str]:
    """Load Future1 members from ExportedMetadata_Future1.csv"""
    csv_file = Path("ExportedMetadata_Future1.csv")
    future1_members = []
    if csv_file.exists():
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
        for encoding in encodings:
            try:
                with open(csv_file, "r", encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    fieldnames = reader.fieldnames
                    if fieldnames:
                        future1_col = fieldnames[0]  # First column
                        for row in reader:
                            future1 = row.get(future1_col, "").strip()
                            if future1 and future1 != future1_col:
                                future1_members.append(future1)
                    break
            except Exception:
                if encoding == encodings[-1]:
                    raise
                continue
    return future1_members if future1_members else ["No Future1"]

def load_entities_from_csv() -> List[str]:
    """Load entity names from ExportedMetadata_Entity.csv"""
    csv_file = Path("ExportedMetadata_Entity.csv")
    entities = []
    if csv_file.exists():
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
        for encoding in encodings:
            try:
                with open(csv_file, "r", encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    # Get the first column name (should be "Entity")
                    fieldnames = reader.fieldnames
                    if fieldnames:
                        entity_col = fieldnames[0]  # First column
                        for row in reader:
                            entity = row.get(entity_col, "").strip()
                            if entity and entity != entity_col:  # Skip header
                                entities.append(entity)
                    break
            except Exception as e:
                print(f"  [WARNING] Error loading entities: {e}")
                if encoding == encodings[-1]:
                    raise
                continue
    return entities if entities else ["Total Entity"]

async def get_revenue_value(
    account: str,
    entity: str,
    scenario: str,
    year: str,
    period: str = "Dec"
) -> Optional[float]:
    """Get revenue value using export_data_slice with correct format"""
    # Include all 10 required dimensions in POV - ORDER MATTERS!
    # Order from FinPlan app: Account, CostCenter, Currency, Entity, Future1, Period, Region, Scenario, Version, Years
    currency = "USD"
    future1 = "No Future1"
    costcenter = "Total CostCenter"
    region = "Total Region"
    version = "Working"
    
    # Correct format: POV as object with members, columns/rows as array of objects with members
    # 10 dimensions in EXACT order from application
    grid_definition = {
        "suppressMissingBlocks": True,
        "pov": {
            "members": [
                [account],      # 1. Account
                [costcenter],   # 2. CostCenter
                [currency],     # 3. Currency
                [entity],       # 4. Entity  
                [future1],      # 5. Future1
                [period],       # 6. Period
                [region],       # 7. Region
                [scenario],     # 8. Scenario
                [version],      # 9. Version
                [year]          # 10. Years
            ]
        },
        "columns": [
            {
                "members": [["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
            }
        ],
        "rows": [
            {
                "members": [[account], [costcenter], [region]]
            }
        ]
    }
    
    arguments = {
        "plan_type": "FinPlan",
        "grid_definition": grid_definition
    }
    
    try:
        result = await execute_tool("export_data_slice", arguments)
        if result.get("status") == "success":
            data = result.get("data", {})
            rows = data.get("rows", [])
            if rows and rows[0].get("data"):
                # Get the last value (Dec/YTD)
                values = rows[0]["data"]
                # Filter out None values and get the last one
                valid_values = [v for v in values if v is not None]
                if valid_values:
                    return float(valid_values[-1])
            else:
                print(f"  [WARNING] No data returned for {account} {entity} {year} {scenario}")
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"  [ERROR] API error for {account} {entity} {year} {scenario}")
            # Extract detailed error message if available
            if "detail" in str(error_msg) or "row" in str(error_msg).lower():
                # Try to parse JSON error if available
                import json as json_lib
                try:
                    if "{" in error_msg:
                        error_json = json_lib.loads(error_msg.split("{")[1].split("}")[0] if "}" in error_msg else error_msg)
                        if "detail" in error_json:
                            print(f"    Detail: {error_json['detail'][:300]}")
                except Exception:
                    pass
            print(f"    Error: {error_msg[:400]}")
    except Exception as e:
        print(f"  [ERROR] Exception retrieving {account} for {entity} ({year} {scenario}): {str(e)}")
        import traceback
        traceback.print_exc()
    return None

async def analyze_revenue_variance():
    """Analyze revenue variance drivers for FY25"""
    print("=" * 80)
    print("REVENUE VARIANCE DRIVERS ANALYSIS - FY25")
    print("=" * 80)
    print()
    
    await initialize_agent()
    print("[OK] Connected to Planning application")
    print()
    
    # Load dimensions from CSV files
    scenarios = load_scenarios_from_csv()
    entities = load_entities_from_csv()
    currencies = load_currencies_from_csv()
    future1_members = load_future1_from_csv()
    costcenters = load_costcenters_from_csv()
    regions = load_regions_from_csv()
    versions = load_versions_from_csv()
    
    print(f"Loaded {len(scenarios)} scenarios: {', '.join(scenarios)}")
    print(f"Loaded {len(entities)} entities")
    print(f"Loaded {len(currencies)} currencies: {', '.join(currencies[:5])}...")
    print(f"Loaded {len(future1_members)} Future1 members: {', '.join(future1_members[:5])}...")
    print(f"Loaded {len(costcenters)} CostCenters: {', '.join(costcenters[:5])}...")
    print(f"Loaded {len(regions)} Regions: {', '.join(regions[:5])}...")
    print(f"Loaded {len(versions)} Versions: {', '.join(versions[:5])}...")
    print()
    
    # Key entities to analyze - use actual entity names from CSV
    # Check what entities are available
    print("Available top-level entities:")
    top_entities = [e for e in entities if e in ["Total Entity", "All Entity"]]
    for e in top_entities[:5]:  # Show first 5
        print(f"  - {e}")
    print()
    
    # Use Total Entity or All Entity if available, otherwise use first entity
    if "Total Entity" in entities:
        entities_to_analyze = ["Total Entity"]
    elif "All Entity" in entities:
        entities_to_analyze = ["All Entity"]
    else:
        entities_to_analyze = [entities[0]] if entities else ["Total Entity"]
    
    print(f"Entities to analyze: {entities_to_analyze}")
    print()
    
    # Revenue account - use total revenue (400000) or rooms revenue (410000)
    revenue_account = "400000"  # Total Revenue
    
    print("Retrieving revenue data...")
    print()
    
    results = {}
    
    # Get data for each entity
    for entity in entities_to_analyze:
        print(f"Processing {entity}...")
        entity_data = {}
        
        # Get FY25 Actual
        fy25_actual = await get_revenue_value(
            revenue_account, entity, "Actual", "FY25", "Dec"
        )
        entity_data["fy25_actual"] = fy25_actual
        
        # Get FY24 Actual
        fy24_actual = await get_revenue_value(
            revenue_account, entity, "Actual", "FY24", "Dec"
        )
        entity_data["fy24_actual"] = fy24_actual
        
        # Get FY25 Budget
        fy25_budget = await get_revenue_value(
            revenue_account, entity, "Budget", "FY25", "Dec"
        )
        entity_data["fy25_budget"] = fy25_budget
        
        # Calculate variances
        if fy25_actual is not None and fy24_actual is not None:
            variance_amount = fy25_actual - fy24_actual
            variance_pct = (variance_amount / abs(fy24_actual) * 100) if fy24_actual != 0 else None
            entity_data["variance_vs_fy24"] = {
                "amount": variance_amount,
                "percent": variance_pct
            }
        
        if fy25_actual is not None and fy25_budget is not None:
            variance_amount = fy25_actual - fy25_budget
            variance_pct = (variance_amount / abs(fy25_budget) * 100) if fy25_budget != 0 else None
            entity_data["variance_vs_budget"] = {
                "amount": variance_amount,
                "percent": variance_pct
            }
        
        results[entity] = entity_data
        
        # Print summary
        if fy25_actual is not None:
            print(f"  FY25 Actual: ${fy25_actual:,.2f}")
        if fy24_actual is not None:
            print(f"  FY24 Actual: ${fy24_actual:,.2f}")
        if entity_data.get("variance_vs_fy24"):
            var = entity_data["variance_vs_fy24"]
            print(f"  Variance vs FY24: ${var['amount']:,.2f} ({var['percent']:.2f}%)")
        print()
    
    # Generate summary report
    print("=" * 80)
    print("REVENUE VARIANCE SUMMARY")
    print("=" * 80)
    print()
    
    # Get the first (and likely only) entity result
    total_entity = results.get(list(results.keys())[0], {}) if results else {}
    if total_entity.get("variance_vs_fy24"):
        var = total_entity["variance_vs_fy24"]
        print("Total Revenue Variance (FY25 vs FY24):")
        print(f"  Amount: ${var['amount']:,.2f}")
        print(f"  Percent: {var['percent']:.2f}%")
        print()
    
    # Entity analysis (since this appears to be a hotel/rooms app, not FCCS)
    print("Variance Analysis:")
    entity_variance = []
    for entity_name, entity_data in results.items():
        if entity_data.get("variance_vs_fy24"):
            var = entity_data["variance_vs_fy24"]
            entity_variance.append({
                "name": entity_name,
                "variance": var["amount"],
                "percent": var["percent"]
            })
            print(f"  {entity_name}: ${var['amount']:,.2f} ({var['percent']:.2f}%)")
    
    # Identify main drivers
    if entity_variance:
        print()
        print("Main Variance Drivers:")
        sorted_entities = sorted(entity_variance, key=lambda x: abs(x["variance"]), reverse=True)
        total_var_amount = abs(total_entity.get("variance_vs_fy24", {}).get("amount", 1))
        for i, ent in enumerate(sorted_entities, 1):
            contribution_pct = (abs(ent["variance"]) / total_var_amount * 100) if total_var_amount != 0 else 0
            print(f"  {i}. {ent['name']}: ${ent['variance']:,.2f} ({ent['percent']:.2f}%) - {contribution_pct:.1f}% of total variance")
    
    # Save results to JSON
    output_file = Path("revenue_variance_analysis_fy25.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"Detailed results saved to: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(analyze_revenue_variance())

