"""Tests for adk_integration helpers that wrap google-adk usage."""

from pathlib import Path
from typing import Any, Dict

import pytest

import adk.adk_integration as ai


class DummyProc:
    def __init__(self, code: int) -> None:
        self.returncode = code


def test_get_google_adk_version_present(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _version(_: str) -> str:
        return "9.9.9"

    monkeypatch.setattr(ai.metadata, "version", _version)
    assert ai.get_google_adk_version() == "9.9.9"


def test_get_google_adk_version_absent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _version(_: str) -> str:
        raise ai.metadata.PackageNotFoundError

    monkeypatch.setattr(ai.metadata, "version", _version)
    assert ai.get_google_adk_version() is None


def test_validate_adk_environment_aistudio(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with monkeypatch.context() as m:
        m.setenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")
        m.setenv("GOOGLE_API_KEY", "dummy")
        status = ai.validate_adk_environment()

    assert status["env_mode"] == "aistudio"
    env = status["environment_variables"]  # type: ignore[index]
    assert env["GOOGLE_API_KEY"].startswith("\u2713")
    assert not status["errors"]  # type: ignore[truthy-bool]


def test_validate_adk_environment_vertex(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with monkeypatch.context() as m:
        m.setenv("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
        m.setenv("GOOGLE_CLOUD_PROJECT", "proj-1")
        m.setenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        status = ai.validate_adk_environment()

    assert status["env_mode"] == "vertex"
    env = status["environment_variables"]  # type: ignore[index]
    assert env["GOOGLE_CLOUD_PROJECT"].startswith("\u2713")
    assert env["GOOGLE_CLOUD_LOCATION"].startswith("\u2713")
    assert not status["errors"]  # type: ignore[truthy-bool]


def test_run_adk_web(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: Dict[str, Any] = {}

    def _run(args: list[str], check: bool = False, **kwargs) -> DummyProc:
        calls["args"] = args
        calls["check"] = check
        return DummyProc(0)

    monkeypatch.setattr(ai.subprocess, "run", _run)
    rc = ai.run_adk_web()
    assert rc == 0
    assert calls["args"] == ["adk", "web"]


def test_run_adk_run_no_message(monkeypatch: pytest.MonkeyPatch) -> None:
    recorded: Dict[str, Any] = {}

    def _run(args: list[str], check: bool = False, **kwargs) -> DummyProc:
        recorded["args"] = args
        recorded["check"] = check
        return DummyProc(0)

    monkeypatch.setattr(ai.subprocess, "run", _run)
    rc = ai.run_adk_run("pkgA")
    assert rc == 0
    assert recorded["args"] == ["adk", "run", "pkgA"]


def test_run_adk_run_with_message(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: Dict[str, Any] = {}

    def _run(
        args: list[str], input: bytes, check: bool = False, **kwargs  # noqa: A002
    ) -> DummyProc:
        captured["args"] = args
        captured["input"] = input
        captured["check"] = check
        return DummyProc(0)

    monkeypatch.setattr(ai.subprocess, "run", _run)
    rc = ai.run_adk_run("pkgB", message="hello")
    assert rc == 0
    assert captured["args"] == ["adk", "run", "pkgB"]
    assert captured["input"] == b"hello"


def test_create_adk_agent_skeleton_with_output(tmp_path: Path) -> None:
    pkg = ai.create_adk_agent_skeleton("demo", output=tmp_path)
    # Directory and files
    assert pkg.exists() and pkg.is_dir()
    assert (pkg / "__init__.py").exists()
    assert (pkg / "agent.py").exists()
    assert (pkg / ".env.template").exists()
    # Minimal content checks
    agent_src = (pkg / "agent.py").read_text(encoding="utf-8")
    assert "root_agent = Agent(" in agent_src


def test_create_adk_agent_skeleton_default_cwd(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    # Force Path.cwd() to return tmp_path
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    pkg = ai.create_adk_agent_skeleton("demo2")
    # The default path is now relative to the project root's 'agents' dir.
    expected_path = Path(__file__).resolve().parent.parent.parent / "agents" / "demo2"
    assert pkg == expected_path
    assert pkg.exists()
