"""Unit tests for the ADK Typer CLI commands."""

from pathlib import Path
from typing import Any, Dict, Optional

import pytest
from typer.testing import CliRunner

from adk.cli import app

runner = CliRunner()


@pytest.fixture
def tmp_path_str(tmp_path: Path) -> str:
    return str(tmp_path)


def test_cli_version() -> None:
    result = runner.invoke(app, ["version"])  # prints version and author
    assert result.exit_code == 0
    assert "ADK Toolkit" in result.output
    assert "Version:" in result.output


def test_cli_validate_success(monkeypatch: pytest.MonkeyPatch) -> None:
    # Mock validate_adk_environment to a happy-path status
    def _mock_validate() -> Dict[str, Any]:
        return {
            "python_version": "3.11.x",
            "python_path": "/usr/bin/python",
            "adk_installed": True,
            "adk_version": "1.2.3",
            "env_mode": "aistudio",
            "environment_variables": {"GOOGLE_API_KEY": "\u2713 Set"},
            "warnings": [],
            "errors": [],
        }

    monkeypatch.setattr(
        "adk.cli.validate_adk_environment",
        _mock_validate,
    )

    result = runner.invoke(app, ["validate"])
    assert result.exit_code == 0
    assert "ADK environment looks good" in result.output


def test_cli_validate_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def _mock_validate() -> Dict[str, Any]:
        return {
            "python_version": "3.11.x",
            "python_path": "/usr/bin/python",
            "adk_installed": False,
            "adk_version": None,
            "env_mode": "unset",
            "environment_variables": {},
            "warnings": [],
            "errors": ["Something went wrong"],
        }

    monkeypatch.setattr(
        "adk.cli.validate_adk_environment",
        _mock_validate,
    )

    result = runner.invoke(app, ["validate"])
    assert result.exit_code != 0
    assert "Environment validation failed" in result.output


def test_cli_scaffold_success(tmp_path: Path) -> None:
    # Use the real scaffolder but write into a temporary directory
    pkg_name = "my_agent_pkg"
    result = runner.invoke(app, ["scaffold", pkg_name, "-o", str(tmp_path)])
    assert result.exit_code == 0
    # Ensure the package folder exists
    assert (tmp_path / pkg_name).exists()
    assert "Created package at:" in result.output


def test_cli_web_success(monkeypatch: pytest.MonkeyPatch) -> None:
    def _mock_web() -> int:
        return 0

    monkeypatch.setattr("adk.cli.run_adk_web", _mock_web)

    result = runner.invoke(app, ["web"])
    assert result.exit_code == 0


def test_cli_web_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def _mock_web() -> int:
        return 2

    monkeypatch.setattr("adk.cli.run_adk_web", _mock_web)

    result = runner.invoke(app, ["web"])
    assert result.exit_code == 2


def test_cli_run_success(monkeypatch: pytest.MonkeyPatch) -> None:
    def _mock_run(
        package: str, message: Optional[str] = None
    ) -> int:  # type: ignore[override]
        # verify we receive the same args passed from CLI
        assert package == "pkg1"
        assert message == "hello"
        return 0

    monkeypatch.setattr("adk.cli.run_adk_run", _mock_run)

    result = runner.invoke(app, ["run", "pkg1", "-m", "hello"])
    assert result.exit_code == 0


def test_cli_run_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def _mock_run(
        package: str, message: Optional[str] = None
    ) -> int:  # type: ignore[override]
        return 3

    monkeypatch.setattr("adk.cli.run_adk_run", _mock_run)

    result = runner.invoke(app, ["run", "pkg1"])
    assert result.exit_code == 3


def test_cli_init_alias_calls_scaffold(
    monkeypatch: pytest.MonkeyPatch, tmp_path_str: str
) -> None:
    called: Dict[str, Any] = {}

    def _mock_scaffold(
        *, name: str, output: Optional[Path] = None
    ) -> None:  # type: ignore[override]
        called["name"] = name
        called["output"] = output

    monkeypatch.setattr("adk.cli.scaffold_adk", _mock_scaffold)

    result = runner.invoke(app, ["init", "init_agent", "--output", tmp_path_str])
    assert result.exit_code == 0
    assert called["name"] == "init_agent"
    # Output should be the tmp path we passed in
    assert str(called["output"]) == tmp_path_str
