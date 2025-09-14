"""Validation utilities for the ADK Course package."""

import typer
from rich.console import Console

from .utils import format_error_message, validate_environment

console = Console()


def main() -> None:
    """Provide main entry point for the validation CLI."""
    console.print("\n[bold blue]🔍 ADK Course Environment Validation[/bold blue]")

    try:
        status = validate_environment()

        # Display results
        console.print(
            "\n[green]✅ Environment validation completed successfully![/green]"
        )

        # Show summary
        console.print("\n[cyan]📊 Summary:[/cyan]")
        console.print(f"  - Python: {status['python_version']}")
        console.print(
            f"  - Environment variables: "
            f"{len(status['environment_variables'])} configured"
        )
        google_cloud_status = (
            "✓ Connected" if status["google_cloud_setup"] else "⚠ Not configured"
        )
        console.print(f"  - Google Cloud: {google_cloud_status}")
        console.print(f"  - Warnings: {len(status['warnings'])}")

        if status["warnings"]:
            console.print("\n[yellow]Warnings:[/yellow]")
            for warning in status["warnings"]:
                console.print(f"  [yellow]⚠[/yellow] {warning}")

    except Exception as e:
        console.print(
            f"\n[red]❌ Environment validation failed: "
            f"{format_error_message(e)}[/red]"
        )
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
