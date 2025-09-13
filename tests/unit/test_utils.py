"""Unit tests for the utils module."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from adk_course.exceptions import ConfigurationError, ValidationError
from adk_course.utils import (
    create_agent_config_template,
    ensure_directory,
    format_error_message,
    get_project_root,
    load_config,
    save_config,
    setup_logging,
    validate_environment,
    validate_file_path,
)


class TestSetupLogging:
    """Test cases for setup_logging function."""

    def test_setup_logging_default(self):
        """Test setting up logging with default parameters."""
        # Should not raise any exception
        setup_logging()

    def test_setup_logging_with_file(self, temp_dir):
        """Test setting up logging with log file."""
        log_file = temp_dir / "test.log"
        setup_logging(log_file=log_file)

        assert log_file.exists()


class TestValidateEnvironment:
    """Test cases for validate_environment function."""

    @patch.dict(os.environ, {"GOOGLE_CLOUD_PROJECT": "test-project"})
    @patch("google.auth.default")
    def test_validate_environment_success(self, mock_auth):
        """Test successful environment validation."""
        mock_auth.return_value = (Mock(), "test-project")

        status = validate_environment()

        assert status["python_version"] == sys.version
        assert status["google_cloud_setup"] is True
        assert "GOOGLE_CLOUD_PROJECT" in status["environment_variables"]

    def test_validate_environment_missing_required_vars(self):
        """Test validation fails when required variables are missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValidationError, match="GOOGLE_CLOUD_PROJECT"):
                validate_environment()

    @patch("sys.version_info", (3, 8, 0))
    def test_validate_environment_old_python(self):
        """Test validation fails with old Python version."""
        with pytest.raises(ValidationError, match="Python 3.9 or higher"):
            validate_environment()


class TestConfigFiles:
    """Test cases for configuration file functions."""

    def test_save_and_load_config(self, temp_dir):
        """Test saving and loading configuration."""
        config = {"name": "test", "value": 123}
        config_path = temp_dir / "test.yaml"

        # Save config
        save_config(config, config_path)
        assert config_path.exists()

        # Load config
        loaded_config = load_config(config_path)
        assert loaded_config == config

    def test_load_config_nonexistent_file(self, temp_dir):
        """Test loading non-existent config file."""
        config_path = temp_dir / "nonexistent.yaml"

        with pytest.raises(ConfigurationError, match="Configuration file not found"):
            load_config(config_path)

    def test_save_config_creates_directory(self, temp_dir):
        """Test saving config creates parent directory."""
        config = {"test": "value"}
        config_path = temp_dir / "nested" / "config.yaml"

        save_config(config, config_path)

        assert config_path.exists()
        assert config_path.parent.exists()


class TestUtilityFunctions:
    """Test cases for utility functions."""

    def test_create_agent_config_template(self):
        """Test creating agent config template."""
        template = create_agent_config_template()

        assert "name" in template
        assert "project_id" in template
        assert "model_name" in template
        assert template["name"] == "example-agent"

    def test_format_error_message(self):
        """Test formatting error messages."""
        error = ValueError("Test error message")
        formatted = format_error_message(error)

        assert "ValueError" in formatted
        assert "Test error message" in formatted

    def test_get_project_root(self):
        """Test getting project root."""
        root = get_project_root()
        assert isinstance(root, Path)
        assert root.exists()

    def test_validate_file_path_existing(self, temp_dir):
        """Test validating existing file path."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # Should not raise exception
        validate_file_path(test_file, must_exist=True)

    def test_validate_file_path_nonexistent_required(self, temp_dir):
        """Test validating non-existent file path when required."""
        test_file = temp_dir / "nonexistent.txt"

        with pytest.raises(ValidationError, match="File does not exist"):
            validate_file_path(test_file, must_exist=True)

    def test_validate_file_path_nonexistent_optional(self, temp_dir):
        """Test validating non-existent file path when optional."""
        test_file = temp_dir / "nonexistent.txt"

        # Should not raise exception
        validate_file_path(test_file, must_exist=False)

    def test_validate_file_path_directory(self, temp_dir):
        """Test validating path that points to directory."""
        with pytest.raises(ValidationError, match="Path is not a file"):
            validate_file_path(temp_dir, must_exist=True)

    def test_ensure_directory(self, temp_dir):
        """Test ensuring directory exists."""
        nested_dir = temp_dir / "level1" / "level2"

        ensure_directory(nested_dir)

        assert nested_dir.exists()
        assert nested_dir.is_dir()

    def test_ensure_directory_existing(self, temp_dir):
        """Test ensuring directory that already exists."""
        # Should not raise exception
        ensure_directory(temp_dir)
