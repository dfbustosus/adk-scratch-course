"""ADK Toolkit - A toolkit for building intelligent agents with Google's Agent Development Kit.

This package provides utilities, a command-line interface, and a foundational structure
for developing, testing, and deploying agents using Google's ADK.
"""

from .core import Agent, AgentConfig, BasicAgent
from .exceptions import ADKError, ConfigurationError, ValidationError
from .utils import setup_logging, validate_environment

try:
    from ._version import __version__
except ImportError:
    # Fallback version if setuptools-scm is not available
    __version__ = "0.1.0"

__author__ = "ADK Toolkit Contributors"
__email__ = "davidbustosusta@gmail.com"
__license__ = "Apache License 2.0"

__all__ = [
    "Agent",
    "AgentConfig",
    "BasicAgent",
    "setup_logging",
    "validate_environment",
    "ADKError",
    "ConfigurationError",
    "ValidationError",
]
