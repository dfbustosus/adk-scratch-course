"""
ADK Course - A comprehensive course on Google Development Kit (GDK) for 
building intelligent agents.

This package provides utilities, examples, and tools for learning and 
implementing Google Development Kit agents and AI systems.
"""

from .core import Agent, AgentConfig, BasicAgent
from .exceptions import ADKError, ConfigurationError, ValidationError
from .utils import setup_logging, validate_environment

try:
    from ._version import __version__
except ImportError:
    # Fallback version if setuptools-scm is not available
    __version__ = "0.1.0"

__author__ = "ADK Course Contributors"
__email__ = "contributors@adk-course.dev"
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