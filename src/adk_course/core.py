"""Core classes and functionality for ADK Course agents."""

import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from google.cloud import aiplatform
from pydantic import BaseModel, ConfigDict, Field

from .exceptions import AgentError, ConfigurationError
from .utils import setup_logging

logger = logging.getLogger(__name__)


class AgentConfig(BaseModel):
    """Configuration for an ADK Agent.

    This class defines the configuration parameters for creating and running
    agents in the Google Development Kit environment.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )

    # Basic configuration
    name: str = Field(..., description="Agent name")
    description: str = Field("", description="Agent description")
    version: str = Field("1.0.0", description="Agent version")

    # Google Cloud configuration
    project_id: str = Field(..., description="Google Cloud project ID")
    location: str = Field("us-central1", description="Google Cloud location")

    # Model configuration
    model_name: str = Field("gemini-pro", description="Model to use")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Model temperature")
    max_tokens: int = Field(1024, ge=1, le=8192, description="Maximum tokens")
    top_p: float = Field(0.9, ge=0.0, le=1.0, description="Top-p sampling")
    top_k: int = Field(40, ge=1, le=100, description="Top-k sampling")

    # Agent behavior
    system_prompt: str = Field("", description="System prompt for the agent")
    max_retries: int = Field(3, ge=0, le=10, description="Maximum retry attempts")
    timeout: float = Field(
        30.0, ge=1.0, le=300.0, description="Request timeout in seconds"
    )

    # Advanced settings
    enable_safety: bool = Field(True, description="Enable safety filters")
    enable_logging: bool = Field(True, description="Enable request logging")
    custom_parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Custom parameters"
    )

    def validate_config(self) -> None:
        """Validate the configuration.

        Raises:
            ConfigurationError: If configuration is invalid
        """
        if not self.project_id:
            raise ConfigurationError("project_id is required", "project_id")

        if not self.name:
            raise ConfigurationError("Agent name is required", "name")

        if self.temperature < 0 or self.temperature > 2:
            raise ConfigurationError(
                "Temperature must be between 0 and 2", "temperature"
            )


@dataclass
class AgentMessage:
    """Represents a message in agent communication."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    role: str = "user"  # user, assistant, system
    content: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class Agent(ABC):
    """Base class for all ADK agents.

    This abstract class defines the interface that all agents must implement.
    It provides common functionality for agent initialization, configuration,
    and basic operations.
    """

    def __init__(self, config: AgentConfig):
        """Initialize the agent.

        Args:
            config: Agent configuration

        Raises:
            ConfigurationError: If configuration is invalid
        """
        config.validate_config()
        self.config = config
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.session_history: List[AgentMessage] = []

        if config.enable_logging:
            setup_logging()

        logger.info(f"Initialized agent '{config.name}' with ID: {self.id}")

        # Initialize Google Cloud AI Platform
        try:
            aiplatform.init(project=config.project_id, location=config.location)
            logger.info(f"Connected to Google Cloud project: {config.project_id}")
        except Exception as e:
            raise ConfigurationError(f"Failed to initialize Google Cloud: {e}")

    @abstractmethod
    async def process_message(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Process a message and return a response.

        Args:
            message: Input message to process
            context: Optional context for processing

        Returns:
            Agent response

        Raises:
            AgentError: If processing fails
        """
        pass

    def add_message(self, message: AgentMessage) -> None:
        """Add a message to the session history.

        Args:
            message: Message to add
        """
        self.session_history.append(message)
        logger.debug(f"Added message to history: {message.id}")

    def get_history(self, limit: Optional[int] = None) -> List[AgentMessage]:
        """Get session history.

        Args:
            limit: Maximum number of messages to return

        Returns:
            List of messages
        """
        if limit is None:
            return self.session_history.copy()
        return self.session_history[-limit:]

    def clear_history(self) -> None:
        """Clear session history."""
        self.session_history.clear()
        logger.info("Cleared session history")

    def get_status(self) -> Dict[str, Any]:
        """Get agent status information.

        Returns:
            Status dictionary
        """
        return {
            "id": self.id,
            "name": self.config.name,
            "created_at": self.created_at.isoformat(),
            "message_count": len(self.session_history),
            "config": self.config.model_dump(),
        }


class BasicAgent(Agent):
    """A basic implementation of the Agent class.

    This agent provides a simple implementation for demonstration and testing.
    It can be used as a starting point for more complex agent implementations.
    """

    async def process_message(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Process a message using the configured model.

        Args:
            message: Input message to process
            context: Optional context for processing

        Returns:
            Agent response

        Raises:
            AgentError: If processing fails
        """
        try:
            # Create user message
            user_message = AgentMessage(role="user", content=message)
            self.add_message(user_message)

            # For now, return a simple echo response
            # In a real implementation, this would use the GDK API
            response_content = f"Agent \"{self.config.name}\" received: {message}"

            # Create assistant response
            assistant_message = AgentMessage(role="assistant", content=response_content)
            self.add_message(assistant_message)

            logger.info(f"Processed message for agent: {self.config.name}")
            return response_content

        except Exception as e:
            raise AgentError(f"Failed to process message: {e}", self.id)

    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation.

        Returns:
            Conversation summary
        """
        if not self.session_history:
            return "No conversation history available."

        messages = [f"{msg.role}: {msg.content}" for msg in self.session_history[-10:]]
        return "\n".join(messages)
