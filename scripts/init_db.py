"""Database initialization script for planning_agent database."""

import sys

from planning_agent.config import PlanningConfig
from planning_agent.services.feedback_service import FeedbackService


def init_schema(db_url: str) -> bool:
    """Initialize the database schema (create tables).

    Args:
        db_url: Full database URL

    Returns:
        True if schema was initialized successfully, False on error
    """
    try:
        print("Initializing database schema...")
        # Initialize feedback service (creates feedback tables)
        feedback_service = FeedbackService(db_url)

        # Initialize RL service tables
        from planning_agent.services.rl_service import RLService
        RLService(feedback_service, db_url)

        print("Database schema initialized successfully.")
        print("Created tables:")
        print("  - tool_executions")
        print("  - tool_metrics")
        print("  - rl_policy")
        print("  - rl_episodes")
        return True
    except Exception as e:
        print(f"Error initializing schema: {e}")
        return False


def main():
    """Main function to initialize the database."""
    print("=" * 60)
    print("Planning Agent Database Initialization")
    print("=" * 60)
    print()

    # Load configuration
    try:
        config = PlanningConfig()
        db_url = config.database_url
        print(f"Database URL: {db_url}")
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print("\nPlease ensure you have a .env file or set DATABASE_URL environment variable.")
        sys.exit(1)

    # Initialize schema (SQLite creates file automatically)
    print("\nInitializing database schema...")
    if not init_schema(db_url):
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Database initialization completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
