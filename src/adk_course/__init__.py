"""
ADK Course - A comprehensive course on Google Development Kit (GDK) for building intelligent agents.

This package provides utilities, examples, and tools for learning and implementing
Google Development Kit agents and AI systems.
"""

__version__ = "1.0.0"
__author__ = "ADK Course Contributors"
__email__ = "contributors@adk-course.dev"
__license__ = "Apache License 2.0"

from .core import Agent, AgentConfig
from .utils import setup_logging, validate_environment
from .exceptions import ADKError, ConfigurationError, ValidationError

__all__ = [
    "Agent",
    "AgentConfig", 
    "setup_logging",
    "validate_environment",
    "ADKError",
    "ConfigurationError",
    "ValidationError",
]