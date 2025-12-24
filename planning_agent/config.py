"""Configuration module using Pydantic Settings."""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class PlanningConfig(BaseSettings):
    """Planning configuration with environment variable validation."""

    # Planning Connection (optional in mock mode)
    planning_url: Optional[str] = Field(None, alias="PLANNING_URL")
    planning_username: Optional[str] = Field(None, alias="PLANNING_USERNAME")
    planning_password: Optional[str] = Field(None, alias="PLANNING_PASSWORD")
    planning_api_version: str = Field("v3", alias="PLANNING_API_VERSION")
    planning_mock_mode: bool = Field(False, alias="PLANNING_MOCK_MODE")

    # Database (SQLite for sessions + feedback + RL)
    database_url: str = Field(
        "sqlite:///./planning_agent.db",
        alias="DATABASE_URL"
    )

    # Gemini Model
    google_api_key: Optional[str] = Field(None, alias="GOOGLE_API_KEY")
    model_id: str = Field("gemini-2.0-flash", alias="MODEL_ID")

    # Server
    port: int = Field(8080, alias="PORT")

    # Reinforcement Learning Configuration
    rl_enabled: bool = Field(True, alias="RL_ENABLED")
    rl_exploration_rate: float = Field(0.1, alias="RL_EXPLORATION_RATE")
    rl_learning_rate: float = Field(0.1, alias="RL_LEARNING_RATE")
    rl_discount_factor: float = Field(0.9, alias="RL_DISCOUNT_FACTOR")
    rl_min_samples: int = Field(5, alias="RL_MIN_SAMPLES")  # Minimum samples before using RL

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "populate_by_name": True,
    }


def load_config() -> PlanningConfig:
    """Load and validate configuration from environment variables."""
    config = PlanningConfig()

    # Don't validate credentials at load time - let the client handle it
    # This allows the module to load even if credentials are missing
    # Validation will happen when PlanningClient is initialized

    return config


# Global config instance - load without strict validation
# Validation happens when PlanningClient is created
# If loading fails, create a default config with mock mode enabled
try:
    config = load_config()
except Exception as e:
    # If config loading fails, create a minimal config with mock mode enabled
    import warnings
    warnings.warn(f"Config loading failed: {e}. Using default mock mode configuration.", UserWarning)
    # Create a new config instance with mock mode enabled
    config = PlanningConfig(
        planning_mock_mode=True,
        database_url="sqlite:///./planning_agent.db"
    )


