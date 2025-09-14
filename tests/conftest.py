"""Test configuration and fixtures for ADK tests."""

import os
import sys
import tempfile
import types
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Ensure local src/ is importable without installing the package
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# Provide a lightweight stub for google.cloud.aiplatform if missing
if "google" not in sys.modules:
    sys.modules["google"] = types.ModuleType("google")
if "google.cloud" not in sys.modules:
    cloud_mod = types.ModuleType("google.cloud")
    sys.modules["google.cloud"] = cloud_mod
    sys.modules["google"].cloud = cloud_mod
if "google.cloud.aiplatform" not in sys.modules:
    ai_mod = types.ModuleType("google.cloud.aiplatform")

    def _init_stub(*args, **kwargs):
        return None

    ai_mod.init = _init_stub
    sys.modules["google.cloud.aiplatform"] = ai_mod

# Stub google.auth.default used by utils.validate_environment
if "google.auth" not in sys.modules:
    auth_mod = types.ModuleType("google.auth")

    def _default_stub():
        return (Mock(), "test-project")

    auth_mod.default = _default_stub  # type: ignore[attr-defined]
    sys.modules["google.auth"] = auth_mod
    # attach to google package as attribute for attribute traversal
    sys.modules["google"].auth = auth_mod

from adk.core import AgentConfig, BasicAgent  # noqa: E402
from adk.utils import create_agent_config_template  # noqa: E402


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
