"""ADK Agent - Main agent definition with all Planning tools."""

import sys
from typing import Any, Optional

from planning_agent.config import config, PlanningConfig
from planning_agent.client.planning_client import PlanningClient
from planning_agent.services.feedback_service import (
    init_feedback_service,
    before_tool_callback,
    after_tool_callback,
    get_feedback_service
)
from planning_agent.services.rl_service import (
    init_rl_service,
    get_rl_service
)

# Import all tool modules
from planning_agent.tools import application, jobs, dimensions, data, variables, documents, snapshots, feedback
from planning_agent.tools.feedback import track_last_execution

# Global state
_planning_client: Optional[PlanningClient] = None
_app_name: Optional[str] = None
_session_state: dict[str, dict[str, Any]] = {}  # Track session state for RL


def get_client() -> PlanningClient:
    """Get the Planning client instance."""
    global _planning_client
    if _planning_client is None:
        _planning_client = PlanningClient(config)
    return _planning_client


def get_app_name() -> Optional[str]:
    """Get the current application name."""
    return _app_name


async def initialize_agent(cfg: Optional[PlanningConfig] = None) -> str:
    """Initialize the agent and connect to Planning.

    Returns:
        str: The application name or error message.
    """
    global _planning_client, _app_name

    use_config = cfg or config

    # Initialize Planning client (with error handling)
    try:
        _planning_client = PlanningClient(use_config)
    except ValueError as e:
        # If credentials are missing and not in mock mode, provide helpful error
        error_msg = str(e)
        print(f"Planning client initialization error: {error_msg}", file=sys.stderr)
        if not use_config.planning_mock_mode:
            print("Hint: Set PLANNING_MOCK_MODE=true to use mock data without credentials", file=sys.stderr)
            print("Attempting to continue with limited functionality...", file=sys.stderr)
            # Try to create client in mock mode as fallback
            try:
                use_config.planning_mock_mode = True
                _planning_client = PlanningClient(use_config)
                print("Switched to mock mode due to missing credentials", file=sys.stderr)
            except Exception:
                raise RuntimeError(f"Planning client initialization failed: {error_msg}") from e
        else:
            # If already in mock mode but still failed, re-raise
            raise RuntimeError(f"Planning client initialization failed: {error_msg}") from e

    # Set client reference in all tool modules
    application.set_client(_planning_client)
    jobs.set_client(_planning_client)
    dimensions.set_client(_planning_client)
    data.set_client(_planning_client)
    variables.set_client(_planning_client)
    documents.set_client(_planning_client)
    snapshots.set_client(_planning_client)

    # Initialize feedback service (optional - don't break if it fails)
    feedback_service = None
    try:
        feedback_service = init_feedback_service(use_config.database_url)
        print("Feedback service initialized", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Could not initialize feedback service: {e}", file=sys.stderr)
        print("Tool execution will continue without feedback tracking", file=sys.stderr)
        # Set feedback service to None so callbacks know it's not available
        import planning_agent.services.feedback_service as feedback_module
        feedback_module._feedback_service = None

    # Initialize RL service (optional - only if feedback service is available and RL enabled)
    if use_config.rl_enabled and feedback_service:
        try:
            init_rl_service(
                feedback_service,
                use_config.database_url,
                exploration_rate=use_config.rl_exploration_rate,
                learning_rate=use_config.rl_learning_rate,
                discount_factor=use_config.rl_discount_factor,
                min_samples=use_config.rl_min_samples
            )
            print("RL service initialized", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Could not initialize RL service: {e}", file=sys.stderr)
            print("RL features will be disabled", file=sys.stderr)

    # Try to connect to Planning and get application name
    try:
        print("Connecting to Planning to retrieve application info...", file=sys.stderr)
        apps = await _planning_client.get_applications()
        if apps and apps.get("items") and len(apps["items"]) > 0:
            _app_name = apps["items"][0]["name"]
            print(f"Connected to Planning Application: {_app_name}", file=sys.stderr)

            # Set app name in tool modules that need it
            jobs.set_app_name(_app_name)
            dimensions.set_app_name(_app_name)
            data.set_app_name(_app_name)
            variables.set_app_name(_app_name)
            documents.set_app_name(_app_name)

            return _app_name
        else:
            print("No applications found", file=sys.stderr)
            return "No applications found"
    except Exception as e:
        print(f"Initialization warning: Could not connect to Planning: {e}", file=sys.stderr)
        return f"Connection failed: {e}"


async def close_agent():
    """Clean up agent resources."""
    global _planning_client
    if _planning_client:
        await _planning_client.close()
        _planning_client = None


# Tool registry - maps tool names to handler functions
TOOL_HANDLERS = {
    # Application
    "get_application_info": application.get_application_info,
    "get_rest_api_version": application.get_rest_api_version,
    # Jobs
    "list_jobs": jobs.list_jobs,
    "get_job_status": jobs.get_job_status,
    "execute_job": jobs.execute_job,
    # Dimensions
    "get_dimensions": dimensions.get_dimensions,
    "get_members": dimensions.get_members,
    "get_member": dimensions.get_member,
    # Data
    "export_data_slice": data.export_data_slice,
    "copy_data": data.copy_data,
    "clear_data": data.clear_data,
    # Variables
    "get_substitution_variables": variables.get_substitution_variables,
    "set_substitution_variable": variables.set_substitution_variable,
    # Documents
    "get_documents": documents.get_documents,
    # Snapshots
    "get_snapshots": snapshots.get_snapshots,
    # Feedback
    "submit_feedback": feedback.submit_feedback,
    "get_recent_executions": feedback.get_recent_executions,
    "rate_last_tool": feedback.rate_last_tool,
}

# Collect all tool definitions
ALL_TOOL_DEFINITIONS = (
    application.TOOL_DEFINITIONS +
    jobs.TOOL_DEFINITIONS +
    dimensions.TOOL_DEFINITIONS +
    data.TOOL_DEFINITIONS +
    variables.TOOL_DEFINITIONS +
    documents.TOOL_DEFINITIONS +
    snapshots.TOOL_DEFINITIONS +
    feedback.TOOL_DEFINITIONS
)


async def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
    session_id: str = "default",
    user_query: str = "",
    use_rl: bool = True
) -> dict[str, Any]:
    """Execute a tool by name with given arguments.

    Args:
        tool_name: Name of the tool to execute.
        arguments: Arguments to pass to the tool.
        session_id: Session ID for feedback tracking.
        user_query: Optional user query for RL context.
        use_rl: Whether to use RL for learning (default: True).

    Returns:
        dict: Tool execution result with optional RL metadata.
    """
    handler = TOOL_HANDLERS.get(tool_name)
    if not handler:
        return {"status": "error", "error": f"Unknown tool: {tool_name}"}

    # Initialize session state if needed
    if session_id not in _session_state:
        _session_state[session_id] = {
            "tool_sequence": [],
            "previous_tool": None,
            "session_length": 0,
            "user_query": user_query
        }

    session_state = _session_state[session_id]
    previous_tool = session_state["previous_tool"]
    session_length = session_state["session_length"]

    # Track execution start (non-blocking)
    try:
        before_tool_callback(session_id, tool_name, arguments)
    except Exception:
        pass  # Ignore feedback service errors

    # Get RL service for context and learning
    rl_service = get_rl_service() if use_rl else None
    context_hash = None
    
    if rl_service:
        try:
            # Create context hash for RL
            context_hash = rl_service.tool_selector.create_context_hash(
                user_query or session_state.get("user_query", ""),
                previous_tool,
                session_length
            )
        except Exception:
            pass  # Continue without RL context

    try:
        result = await handler(**arguments)

        # Update session state FIRST (needed for next context hash calculation)
        session_state["tool_sequence"].append(tool_name)
        session_state["previous_tool"] = tool_name
        session_state["session_length"] += 1

        # Track execution end (non-blocking)
        # This will also trigger RL policy update via feedback_service callback
        try:
            execution_id = after_tool_callback(session_id, tool_name, arguments, result, context_hash)
            
            # Track last execution for rate_last_tool
            if execution_id:
                track_last_execution(session_id, execution_id, tool_name, context_hash)

            # Update RL policy with context if available
            if rl_service and context_hash and execution_id:
                try:
                    # Get execution from feedback service to calculate reward
                    feedback_service = get_feedback_service()
                    if feedback_service:
                        from planning_agent.services.feedback_service import ToolExecution
                        with feedback_service.Session() as session:
                            execution = session.get(ToolExecution, execution_id)
                            if execution:
                                execution_doc = {
                                    "success": execution.success,
                                    "user_rating": execution.user_rating,
                                    "execution_time_ms": execution.execution_time_ms,
                                    "tool_name": execution.tool_name
                                }
                                reward = rl_service.calculate_reward(execution_doc)

                                # Calculate next context hash for Q-learning
                                next_context_hash = rl_service.tool_selector.create_context_hash(
                                    session_state.get("user_query", ""),
                                    session_state["previous_tool"],
                                    session_state["session_length"]
                                )

                                # Get available tools for max Q calculation
                                available_tools = list(TOOL_HANDLERS.keys())

                                # Q-learning update with next state
                                rl_service.update_policy(
                                    session_id,
                                    tool_name,
                                    context_hash,
                                    reward,
                                    next_context_hash=next_context_hash,
                                    available_tools=available_tools,
                                    is_terminal=False
                                )
                except Exception:
                    pass  # Silently fail RL updates
        except Exception:
            pass  # Ignore feedback service errors

        # Add RL metadata to result if available
        if rl_service and context_hash:
            try:
                confidence = rl_service.get_tool_confidence(tool_name, context_hash)
                result["rl_metadata"] = {
                    "confidence": confidence,
                    "context_hash": context_hash
                }
            except Exception:
                pass

        return result
    except Exception as e:
        error_result = {"status": "error", "error": str(e)}
        try:
            after_tool_callback(session_id, tool_name, arguments, error_result, context_hash)
        except Exception:
            pass  # Ignore feedback service errors

        # Update session state even on error
        session_state["tool_sequence"].append(tool_name)
        session_state["previous_tool"] = tool_name
        session_state["session_length"] += 1

        return error_result


async def execute_tool_with_rl(
    tool_name: str,
    arguments: dict[str, Any],
    session_id: str = "default",
    user_query: str = ""
) -> dict[str, Any]:
    """Execute tool with RL-enhanced recommendations.
    
    This is a convenience wrapper that:
    1. Gets RL recommendations before execution
    2. Executes the tool
    3. Updates RL policy after execution
    
    Args:
        tool_name: Name of the tool to execute.
        arguments: Arguments to pass to the tool.
        session_id: Session ID for feedback tracking.
        user_query: User query for RL context.
        
    Returns:
        dict: Tool execution result with RL recommendations.
    """
    rl_service = get_rl_service()
    recommendations = None
    
    if rl_service:
        try:
            session_state = _session_state.get(session_id, {})
            recommendations = rl_service.get_tool_recommendations(
                user_query=user_query or session_state.get("user_query", ""),
                previous_tool=session_state.get("previous_tool"),
                session_length=session_state.get("session_length", 0),
                available_tools=list(TOOL_HANDLERS.keys())
            )
        except Exception:
            pass  # Continue without recommendations
    
    # Execute tool
    result = await execute_tool(tool_name, arguments, session_id, user_query, use_rl=True)
    
    # Add recommendations to result if available
    if recommendations:
        result["rl_recommendations"] = recommendations[:5]  # Top 5 recommendations
    
    return result


def finalize_session(session_id: str, outcome: str = "success"):
    """Finalize a session and log episode for RL learning.

    This applies a terminal reward to the last action and logs the episode.

    Args:
        session_id: Session ID to finalize.
        outcome: Session outcome ('success', 'partial', 'failure').
    """
    if session_id not in _session_state:
        return

    session_state = _session_state[session_id]
    tool_sequence = session_state.get("tool_sequence", [])

    if not tool_sequence:
        return

    rl_service = get_rl_service()
    if rl_service:
        try:
            # Calculate episode reward based on outcome
            episode_reward = 10.0 if outcome == "success" else (5.0 if outcome == "partial" else -5.0)

            # Apply terminal reward to the last action in the sequence
            # This ensures the final action gets credit for session success/failure
            last_tool = tool_sequence[-1]
            last_context_hash = rl_service.tool_selector.create_context_hash(
                session_state.get("user_query", ""),
                tool_sequence[-2] if len(tool_sequence) > 1 else None,
                len(tool_sequence) - 1
            )

            # Terminal update - no future rewards (is_terminal=True)
            rl_service.update_policy(
                session_id,
                last_tool,
                last_context_hash,
                episode_reward,
                next_context_hash=None,
                available_tools=list(TOOL_HANDLERS.keys()),
                is_terminal=True
            )

            # Log the complete episode for sequence learning
            rl_service.log_episode(
                session_id,
                tool_sequence,
                episode_reward,
                outcome
            )
        except Exception:
            pass  # Silently fail
    
    # Clean up session state (keep for a while in case of late feedback)
    # Could implement TTL cleanup later


def get_tool_definitions() -> list[dict]:
    """Get all tool definitions for MCP server."""
    return ALL_TOOL_DEFINITIONS


# Agent instruction for ADK
AGENT_INSTRUCTION = """You are an expert assistant for Oracle EPM Cloud Planning.

You help users with:
- Querying planning data from Planning cubes
- Running business rules and jobs
- Managing dimensions and metadata
- Working with substitution variables
- Accessing library documents and snapshots
- Exporting and importing data

Respond in the same language as the user (English or Portuguese).
Always provide clear explanations of what you're doing and the results.

IMPORTANT - Feedback Collection:
After completing a tool execution that returns data or performs an action, 
briefly ask the user: "Was this result helpful?"
- If they say yes/good/helpful/correct, call rate_last_tool with rating="good"
- If they say no/bad/wrong/unhelpful, call rate_last_tool with rating="bad"
This feedback improves future tool recommendations through reinforcement learning.

Available tools:
- get_application_info: Get Planning application details
- list_jobs, get_job_status, execute_job: Monitor and execute jobs
- get_dimensions, get_members, get_member: Explore dimensions
- export_data_slice, copy_data, clear_data: Query and manage data
- get_substitution_variables, set_substitution_variable: Manage variables
- get_documents: Access library documents
- get_snapshots: List application snapshots
- rate_last_tool: Quick feedback on last tool (good/bad)
- submit_feedback, get_recent_executions: Detailed feedback for RL learning
"""













