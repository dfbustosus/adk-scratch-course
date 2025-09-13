"""Unit tests for the core module."""

import uuid
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from adk_course.core import AgentConfig, AgentMessage, BasicAgent
from adk_course.exceptions import AgentError, ConfigurationError


class TestAgentConfig:
    """Test cases for AgentConfig class."""

    def test_agent_config_creation(self):
        """Test creating a valid agent configuration."""
        config = AgentConfig(name="test-agent", project_id="test-project")

        assert config.name == "test-agent"
        assert config.project_id == "test-project"
        assert config.location == "us-central1"  # default value
        assert config.temperature == 0.7  # default value

    def test_agent_config_validation_missing_name(self):
        """Test validation fails when name is missing."""
        with pytest.raises(ConfigurationError, match="Agent name is required"):
            config = AgentConfig(name="", project_id="test-project")
            config.validate_config()

    def test_agent_config_validation_missing_project_id(self):
        """Test validation fails when project_id is missing."""
        with pytest.raises(ConfigurationError, match="project_id is required"):
            config = AgentConfig(name="test-agent", project_id="")
            config.validate_config()

    def test_agent_config_validation_invalid_temperature(self):
        """Test validation fails with invalid temperature."""
        with pytest.raises(
            ConfigurationError, match="Temperature must be between 0 and 2"
        ):
            config = AgentConfig(
                name="test-agent", project_id="test-project", temperature=3.0
            )
            config.validate_config()

    def test_agent_config_valid_config(self):
        """Test validation passes with valid configuration."""
        config = AgentConfig(
            name="test-agent", project_id="test-project", temperature=0.8
        )
        # Should not raise any exception
        config.validate_config()


class TestAgentMessage:
    """Test cases for AgentMessage class."""

    def test_message_creation(self):
        """Test creating an agent message."""
        message = AgentMessage(role="user", content="Hello, world!")

        assert message.role == "user"
        assert message.content == "Hello, world!"
        assert isinstance(message.id, str)
        assert isinstance(message.timestamp, datetime)
        assert message.metadata == {}

    def test_message_to_dict(self):
        """Test converting message to dictionary."""
        message = AgentMessage(role="user", content="Hello, world!")
        message_dict = message.to_dict()

        assert message_dict["role"] == "user"
        assert message_dict["content"] == "Hello, world!"
        assert "id" in message_dict
        assert "timestamp" in message_dict
        assert "metadata" in message_dict

    def test_message_with_metadata(self):
        """Test creating message with metadata."""
        metadata = {"source": "test", "priority": "high"}
        message = AgentMessage(role="assistant", content="Response", metadata=metadata)

        assert message.metadata == metadata
        assert message.to_dict()["metadata"] == metadata


class TestBasicAgent:
    """Test cases for BasicAgent class."""

    @patch("google.cloud.aiplatform.init")
    def test_agent_creation(self, mock_init, sample_config):
        """Test creating a basic agent."""
        agent = BasicAgent(sample_config)

        assert agent.config.name == sample_config.name
        assert isinstance(agent.id, str)
        assert isinstance(agent.created_at, datetime)
        assert agent.session_history == []
        mock_init.assert_called_once()

    @patch("google.cloud.aiplatform.init")
    def test_agent_creation_invalid_config(self, mock_init):
        """Test creating agent with invalid configuration."""
        config = AgentConfig(name="", project_id="test-project")

        with pytest.raises(ConfigurationError):
            BasicAgent(config)

    @patch("google.cloud.aiplatform.init")
    @pytest.mark.asyncio
    async def test_process_message(self, mock_init, sample_config):
        """Test processing a message."""
        agent = BasicAgent(sample_config)

        response = await agent.process_message("Hello, agent!")

        assert "Agent 'test-agent' received: Hello, agent!" in response
        assert len(agent.session_history) == 2  # user + assistant message

        # Check message history
        user_msg = agent.session_history[0]
        assert user_msg.role == "user"
        assert user_msg.content == "Hello, agent!"

        assistant_msg = agent.session_history[1]
        assert assistant_msg.role == "assistant"
        assert "received: Hello, agent!" in assistant_msg.content

    @patch("google.cloud.aiplatform.init")
    def test_add_message(self, mock_init, sample_config):
        """Test adding a message to history."""
        agent = BasicAgent(sample_config)
        message = AgentMessage(role="user", content="Test message")

        agent.add_message(message)

        assert len(agent.session_history) == 1
        assert agent.session_history[0] == message

    @patch("google.cloud.aiplatform.init")
    def test_get_history(self, mock_init, sample_config):
        """Test getting message history."""
        agent = BasicAgent(sample_config)

        # Add some messages
        for i in range(5):
            message = AgentMessage(role="user", content=f"Message {i}")
            agent.add_message(message)

        # Test getting all history
        all_history = agent.get_history()
        assert len(all_history) == 5

        # Test getting limited history
        limited_history = agent.get_history(limit=3)
        assert len(limited_history) == 3
        assert limited_history[0].content == "Message 2"  # Last 3 messages

    @patch("google.cloud.aiplatform.init")
    def test_clear_history(self, mock_init, sample_config):
        """Test clearing message history."""
        agent = BasicAgent(sample_config)

        # Add a message
        message = AgentMessage(role="user", content="Test message")
        agent.add_message(message)
        assert len(agent.session_history) == 1

        # Clear history
        agent.clear_history()
        assert len(agent.session_history) == 0

    @patch("google.cloud.aiplatform.init")
    def test_get_status(self, mock_init, sample_config):
        """Test getting agent status."""
        agent = BasicAgent(sample_config)
        status = agent.get_status()

        assert "id" in status
        assert "name" in status
        assert "created_at" in status
        assert "message_count" in status
        assert "config" in status

        assert status["name"] == sample_config.name
        assert status["message_count"] == 0

    @patch("google.cloud.aiplatform.init")
    def test_get_conversation_summary(self, mock_init, sample_config):
        """Test getting conversation summary."""
        agent = BasicAgent(sample_config)

        # Test empty history
        summary = agent.get_conversation_summary()
        assert "No conversation history available" in summary

        # Add messages
        user_msg = AgentMessage(role="user", content="Hello")
        assistant_msg = AgentMessage(role="assistant", content="Hi there")
        agent.add_message(user_msg)
        agent.add_message(assistant_msg)

        summary = agent.get_conversation_summary()
        assert "user: Hello" in summary
        assert "assistant: Hi there" in summary
