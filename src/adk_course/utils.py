"""Utility functions for the ADK Course package."""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import structlog

from .exceptions import ConfigurationError, ValidationError


def setup_logging(
    level: str = "INFO",
    format_type: str = "json",
    log_file: Optional[Path] = None,
) -> None:
    """Set up structured logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Format type ('json' or 'console')
        log_file: Optional file to write logs to
    """
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            (
                structlog.processors.JSONRenderer()
                if format_type == "json"
                else structlog.dev.ConsoleRenderer(colors=True)
            ),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
    )

    # Add file handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        logging.getLogger().addHandler(file_handler)


def validate_environment() -> Dict[str, Any]:
    """Validate the environment and return status information.

    Returns:
        Dictionary containing validation results

    Raises:
        ValidationError: If critical environment issues are found
    """
    status: Dict[str, Any] = {
        "python_version": sys.version,
        "python_path": sys.executable,
        "working_directory": os.getcwd(),
        "environment_variables": {},
        "google_cloud_setup": False,
        "warnings": [],
        "errors": [],
    }

    # Check Python version
    if sys.version_info < (3, 9):
        status["errors"].append("Python 3.9 or higher is required")

    # Check required environment variables
    required_env_vars = ["GOOGLE_CLOUD_PROJECT"]
    optional_env_vars = [
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GOOGLE_CLOUD_LOCATION",
    ]

    for var in required_env_vars:
        value = os.getenv(var)
        if value:
            status["environment_variables"][var] = "✓ Set"
        else:
            status["errors"].append(f"Required environment variable {var} is not set")

    for var in optional_env_vars:
        value = os.getenv(var)
        if value:
            status["environment_variables"][var] = "✓ Set"
        else:
            status["warnings"].append(f"Optional environment variable {var} is not set")

    # Check Google Cloud setup
    try:
        from google.auth import default

        credentials, project_id = default()
        status["google_cloud_setup"] = True
        status["google_cloud_project"] = project_id
    except Exception as e:
        status["warnings"].append(f"Google Cloud authentication not configured: {e}")

    # Raise error if critical issues found
    if status["errors"]:
        raise ValidationError(
            f"Environment validation failed: {'; '.join(status['errors'])}"
        )

    return status


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from a YAML file.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary

    Raises:
        ConfigurationError: If config file cannot be loaded
    """
    try:
        import yaml

        if not config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            raise ConfigurationError("Configuration file must contain a YAML object")

        return config

    except yaml.YAMLError as e:
        raise ConfigurationError(f"Invalid YAML in configuration file: {e}")
    except Exception as e:
        raise ConfigurationError(f"Failed to load configuration: {e}")


def save_config(config: Dict[str, Any], config_path: Path) -> None:
    """Save configuration to a YAML file.

    Args:
        config: Configuration dictionary
        config_path: Path to save configuration

    Raises:
        ConfigurationError: If config cannot be saved
    """
    try:
        import yaml

        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)

    except Exception as e:
        raise ConfigurationError(f"Failed to save configuration: {e}")


def get_project_root() -> Path:
    """Get the project root directory.

    Returns:
        Path to project root
    """
    current = Path(__file__).resolve()

    # Look for markers that indicate project root
    markers = ["pyproject.toml", "setup.py", ".git", "README.md"]

    for parent in current.parents:
        if any((parent / marker).exists() for marker in markers):
            return parent

    # If no markers found, return current directory
    return Path.cwd()


def create_agent_config_template() -> Dict[str, Any]:
    """Create a template agent configuration.

    Returns:
        Template configuration dictionary
    """
    return {
        "name": "example-agent",
        "description": "An example ADK agent",
        "version": "1.0.0",
        "project_id": "your-google-cloud-project",
        "location": "us-central1",
        "model_name": "gemini-pro",
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 0.9,
        "top_k": 40,
        "system_prompt": "You are a helpful AI assistant.",
        "max_retries": 3,
        "timeout": 30.0,
        "enable_safety": True,
        "enable_logging": True,
        "custom_parameters": {},
    }


def format_error_message(error: Exception) -> str:
    """Format an error message for display.

    Args:
        error: Exception to format

    Returns:
        Formatted error message
    """
    error_type = type(error).__name__
    error_message = str(error)

    return f"{error_type}: {error_message}"


def validate_file_path(file_path: Path, must_exist: bool = True) -> None:
    """Validate a file path.

    Args:
        file_path: Path to validate
        must_exist: Whether the file must exist

    Raises:
        ValidationError: If validation fails
    """
    if must_exist and not file_path.exists():
        raise ValidationError(f"File does not exist: {file_path}")

    if file_path.exists() and not file_path.is_file():
        raise ValidationError(f"Path is not a file: {file_path}")

    # Check if parent directory exists for file creation
    if not must_exist and not file_path.parent.exists():
        raise ValidationError(f"Parent directory does not exist: {file_path.parent}")


def ensure_directory(directory: Path) -> None:
    """Ensure a directory exists, creating it if necessary.

    Args:
        directory: Directory path to ensure
    """
    directory.mkdir(parents=True, exist_ok=True)
