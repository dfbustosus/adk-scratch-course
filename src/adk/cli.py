"""Command-line interface for the ADK Toolkit."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
from rich.console import Console
from rich.table import Table

from .adk_integration import (
    create_adk_agent_skeleton,
    run_adk_run,
    run_adk_web,
    validate_adk_environment,
)
from .exceptions import ADKError
from .utils import format_error_message, setup_logging

app = typer.Typer(
    name="adk",
    help=(
        "A toolkit for building, testing, and deploying intelligent agents with Google's ADK."
    ),
)
console = Console()


@app.command()
def validate() -> None:
    """Validate the ADK development environment (AI Studio / Vertex)."""
    console.print("\n[bold blue]🔍 Validating ADK Environment[/bold blue]")

    try:
        status = validate_adk_environment()

        console.print(f"\n[green]✓[/green] Python: {status['python_version']}")
        console.print(f"[green]✓[/green] Python Path: {status['python_path']}")
        adk_installed = "Yes" if status["adk_installed"] else "No"
        console.print("[green]✓[/green] google-adk installed: " f"{adk_installed}")
        if status["adk_installed"]:
            console.print(
                f"[green]✓[/green] google-adk version: {status['adk_version']}"
            )

        # Environment mode
        console.print(f"Mode: [cyan]{status['env_mode']}[/cyan]")

        # Environment variables table
        env_vars: Dict[str, Any] = status.get("environment_variables", {})
        if env_vars:
            table = Table(title="Environment Variables")
            table.add_column("Variable", style="cyan")
            table.add_column("Status", style="green")
            for var, value in env_vars.items():
                table.add_row(str(var), str(value))
            console.print(table)

        # Warnings / Errors
        warnings: List[str] = status.get("warnings", [])
        if warnings:
            console.print("\n[bold yellow]Warnings:[/bold yellow]")
            for w in warnings:
                console.print(f"[yellow]⚠[/yellow] {w}")

        errors: List[str] = status.get("errors", [])
        if errors:
            console.print("\n[bold red]Errors:[/bold red]")
            for err in errors:
                console.print(f"[red]✖[/red] {err}")

        if status.get("errors"):
            raise ADKError("Environment validation failed")

        console.print("\n[green]✅ ADK environment looks good![/green]")

    except Exception as e:
        error_msg = format_error_message(e)
        console.print(f"\n[red]❌ Environment validation failed: {error_msg}[/red]")
        raise typer.Exit(1)


@app.command("scaffold")
def scaffold_adk(
    name: str = typer.Argument(..., help="ADK agent package name"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output directory (defaults to CWD/name)"
    ),
) -> None:
    """Create an ADK agent package (Quickstart-compliant)."""
    console.print(f"\n[bold blue]🚀 Scaffolding ADK agent: {name}[/bold blue]")
    try:
        pkg_dir = create_adk_agent_skeleton(name, output)
        console.print(f"[green]✓[/green] Created package at: [cyan]{pkg_dir}[/cyan]")
        msg = (
            "\n[cyan]Next steps:[/cyan]\n"
            "  1) cp {pkg}/.env.template {pkg}/.env\n"
            "  2) Fill AI Studio API key OR Vertex AI project/region\n"
            "  3) Run 'adk web' from repo root and select your agent\n"
            "  4) Or run: adk run {pkg_name}\n"
        ).format(pkg=pkg_dir, pkg_name=name)
        console.print(msg)
    except Exception as e:
        console.print(f"[red]❌ Scaffold failed: " f"{format_error_message(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def web() -> None:
    """Launch the ADK Dev UI (equivalent to `adk web`)."""
    console.print("\n[bold blue]🌐 Launching ADK Dev UI[/bold blue]")
    rc = run_adk_web()
    if rc != 0:
        raise typer.Exit(rc)


@app.command()
def run(
    package: str = typer.Argument(..., help="ADK agent package name (folder)"),
    message: Optional[str] = typer.Option(
        None,
        "--message",
        "-m",
        help=("Optional initial message " "piped to the agent"),
    ),
) -> None:
    """Run an ADK agent (equivalent to `adk run <package>`)."""
    console.print(f"\n[bold blue]💬 Running agent:[/bold blue] {package}")
    rc = run_adk_run(package, message)
    if rc != 0:
        raise typer.Exit(rc)


# Deprecated commands retained as aliases for transition
@app.command("init")
def init_alias(name: str, output: Optional[Path] = None) -> None:
    """Deprecated: Use `adk scaffold` instead."""
    console.print(
        "[yellow]`init` is deprecated; using `scaffold` " "under the hood.[/yellow]"
    )
    scaffold_adk(name=name, output=output)


@app.command()
def version() -> None:
    """Display version information."""
    from . import __author__, __version__

    console.print("\n[bold blue]ADK Toolkit[/bold blue]")
    console.print(f"Version: [green]{__version__}[/green]")
    console.print(f"Author: [cyan]{__author__}[/cyan]")
    homepage_url = "https://github.com/dfbustosus/google-adk-toolkit"
    console.print(f"Homepage: [link]{homepage_url}[/link]")


def main() -> None:
    """Serve as main entry point for the CLI."""
    try:
        setup_logging()
        app()
    except ADKError as e:
        console.print(f"[red]❌ ADK Error: {format_error_message(e)}[/red]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[blue]👋 Operation cancelled by user[/blue]")
        raise typer.Exit(0)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {format_error_message(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
