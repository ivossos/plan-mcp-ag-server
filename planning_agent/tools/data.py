"""Data tools - export_data_slice, copy_data, clear_data."""

from typing import Any, Optional

from planning_agent.client.planning_client import PlanningClient

_client: PlanningClient = None
_app_name: str = None


def set_client(client: PlanningClient):
    global _client
    _client = client


def set_app_name(app_name: str):
    global _app_name
    _app_name = app_name


async def export_data_slice(
    plan_type: str,
    grid_definition: dict[str, Any]
) -> dict[str, Any]:
    """Export a specific data slice (grid) from the application / Exportar um slice de dados.

    Args:
        plan_type: The name of the plan type (e.g., 'FinPlan', 'FinRPT').
        grid_definition: The data grid definition with pov, columns, and rows.

    Returns:
        dict: The exported data slice with rows and column values.
    """
    result = await _client.export_data_slice(_app_name, plan_type, grid_definition)
    return {"status": "success", "data": result}


async def copy_data(
    from_scenario: Optional[str] = None,
    to_scenario: Optional[str] = None,
    from_year: Optional[str] = None,
    to_year: Optional[str] = None,
    from_period: Optional[str] = None,
    to_period: Optional[str] = None
) -> dict[str, Any]:
    """Copy data between scenarios, years, or periods / Copiar dados entre cenarios.

    Args:
        from_scenario: Source scenario.
        to_scenario: Target scenario.
        from_year: Source year.
        to_year: Target year.
        from_period: Source period.
        to_period: Target period.

    Returns:
        dict: Job submission result.
    """
    parameters = {}
    if from_scenario:
        parameters["fromScenario"] = from_scenario
    if to_scenario:
        parameters["toScenario"] = to_scenario
    if from_year:
        parameters["fromYear"] = from_year
    if to_year:
        parameters["toYear"] = to_year
    if from_period:
        parameters["fromPeriod"] = from_period
    if to_period:
        parameters["toPeriod"] = to_period

    result = await _client.copy_data(_app_name, parameters)
    return {"status": "success", "data": result}


async def clear_data(
    scenario: Optional[str] = None,
    year: Optional[str] = None,
    period: Optional[str] = None
) -> dict[str, Any]:
    """Clear data for specified scenario, year, and period / Limpar dados.

    Args:
        scenario: Scenario to clear.
        year: Year to clear.
        period: Period to clear.

    Returns:
        dict: Job submission result.
    """
    parameters = {}
    if scenario:
        parameters["scenario"] = scenario
    if year:
        parameters["year"] = year
    if period:
        parameters["period"] = period

    result = await _client.clear_data(_app_name, parameters)
    return {"status": "success", "data": result}


TOOL_DEFINITIONS = [
    {
        "name": "export_data_slice",
        "description": "Export a specific data slice (grid) from the application / Exportar um slice de dados",
        "inputSchema": {
            "type": "object",
            "properties": {
                "plan_type": {
                    "type": "string",
                    "description": "The name of the plan type (e.g., 'FinPlan', 'FinRPT')",
                },
                "grid_definition": {
                    "type": "object",
                    "description": "The data grid definition with pov, columns, and rows",
                },
            },
            "required": ["plan_type", "grid_definition"],
        },
    },
    {
        "name": "copy_data",
        "description": "Copy data between scenarios, years, or periods / Copiar dados entre cenarios",
        "inputSchema": {
            "type": "object",
            "properties": {
                "from_scenario": {"type": "string", "description": "Source scenario"},
                "to_scenario": {"type": "string", "description": "Target scenario"},
                "from_year": {"type": "string", "description": "Source year"},
                "to_year": {"type": "string", "description": "Target year"},
                "from_period": {"type": "string", "description": "Source period"},
                "to_period": {"type": "string", "description": "Target period"},
            },
        },
    },
    {
        "name": "clear_data",
        "description": "Clear data for specified scenario, year, and period / Limpar dados",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scenario": {"type": "string", "description": "Scenario to clear"},
                "year": {"type": "string", "description": "Year to clear"},
                "period": {"type": "string", "description": "Period to clear"},
            },
        },
    },
]


