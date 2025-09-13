"""Custom exceptions for the ADK Course package."""


class ADKError(Exception):
    """Base exception class for all ADK Course related errors."""

    def __init__(self, message: str, code: str | None = None):
        """Initialize ADKError.

        Args:
            message: Error message
            code: Optional error code for categorization
        """
        super().__init__(message)
        self.message = message
        self.code = code


class ConfigurationError(ADKError):
    """Raised when there's an error in configuration."""

    def __init__(self, message: str, config_key: str | None = None):
        """Initialize ConfigurationError.

        Args:
            message: Error message
            config_key: The configuration key that caused the error
        """
        super().__init__(message, "CONFIG_ERROR")
        self.config_key = config_key


class ValidationError(ADKError):
    """Raised when validation fails."""

    def __init__(self, message: str, field: str | None = None):
        """Initialize ValidationError.

        Args:
            message: Error message
            field: The field that failed validation
        """
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field


class AuthenticationError(ADKError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        """Initialize AuthenticationError.

        Args:
            message: Error message
        """
        super().__init__(message, "AUTH_ERROR")


class AgentError(ADKError):
    """Raised when there's an error in agent operations."""

    def __init__(self, message: str, agent_id: str | None = None):
        """Initialize AgentError.

        Args:
            message: Error message
            agent_id: The ID of the agent that caused the error
        """
        super().__init__(message, "AGENT_ERROR")
        self.agent_id = agent_id


class ResourceError(ADKError):
    """Raised when there's an error accessing resources."""

    def __init__(self, message: str, resource_type: str | None = None):
        """Initialize ResourceError.

        Args:
            message: Error message
            resource_type: The type of resource that caused the error
        """
        super().__init__(message, "RESOURCE_ERROR")
        self.resource_type = resource_type
