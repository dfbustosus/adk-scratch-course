"""Test configuration and fixtures for ADK Course tests."""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from adk_course import AgentConfig, BasicAgent
from adk_course.utils import create_agent_config_template


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config():
    """Provide a sample agent configuration."""
    config_dict = create_agent_config_template()
    config_dict["project_id"] = "test-project"
    config_dict["name"] = "test-agent"
    return AgentConfig(**config_dict)


@pytest.fixture
def basic_agent(sample_config):
    """Provide a basic agent instance for testing."""
    with patch("google.cloud.aiplatform.init"):
        agent = BasicAgent(sample_config)
        yield agent


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    env_vars = {
        "GOOGLE_CLOUD_PROJECT": "test-project",
        "GOOGLE_CLOUD_LOCATION": "us-central1",
    }

    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def config_file(temp_dir, sample_config):
    """Create a temporary config file."""
    import yaml

    config_path = temp_dir / "test-config.yaml"
    config_dict = sample_config.model_dump()

    with open(config_path, "w") as f:
        yaml.dump(config_dict, f)

    yield config_path


@pytest.fixture(autouse=True)
def mock_google_auth():
    """Mock Google authentication for all tests."""
    with patch("google.auth.default") as mock_auth:
        mock_auth.return_value = (Mock(), "test-project")
        yield mock_auth
