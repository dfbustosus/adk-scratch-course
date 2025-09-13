"""Setup utilities for the ADK Course package."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from .utils import (
    create_agent_config_template,
    ensure_directory,
    format_error_message,
    save_config,
)

console = Console()


def setup_project(project_path: Optional[Path] = None) -> None:
    """Set up a new ADK Course project."""
    if project_path is None:
        project_path = Path.cwd()
        
    console.print(
        f"\n[bold blue]🚀 Setting up ADK Course project in: {project_path}[/bold blue]"
    )

    try:
        # Create project structure
        directories = [
            "agents",
            "examples",
            "notebooks",
            "data",
            "configs",
            "logs",
        ]

        for dir_name in directories:
            ensure_directory(project_path / dir_name)
            console.print(f"[green]✓[/green] Created directory: {dir_name}/")

        # Create default configuration
        config = create_agent_config_template()
        config_path = project_path / "configs" / "default-agent.yaml"
        save_config(config, config_path)
        console.print(f"[green]✓[/green] Created default configuration: {config_path}")

        # Create .env template
        env_template = """# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# ADK Course Configuration
ADK_LOG_LEVEL=INFO
ADK_LOG_FORMAT=json
"""

        env_path = project_path / ".env.template"
        with open(env_path, "w") as f:
            f.write(env_template)
        console.print(f"[green]✓[/green] Created environment template: {env_path}")

        # Create README
        readme_content = """# ADK Course Project

This is an ADK Course project for learning Google Development Kit (GDK) agents.

## Setup

1. Copy `.env.template` to `.env` and update the values
2. Install dependencies: `pip install -e ".[dev]"`
3. Validate environment: `adk-course validate`

## Directory Structure

- `agents/` - Agent configurations and code
- `examples/` - Example code and demonstrations
- `notebooks/` - Jupyter notebooks for interactive learning
- `data/` - Data files and resources
- `configs/` - Configuration files
- `logs/` - Log files

## Quick Start

1. Initialize a new agent:
   ```bash
   adk-course init my-agent
   ```

2. Test the agent:
   ```bash
   adk-course test --config agents/my-agent/config.yaml
   ```

3. Start interactive chat:
   ```bash
   adk-course chat --config agents/my-agent/config.yaml
   ```

## Learn More

Visit the [ADK Course documentation](https://dfbustosus.github.io/adk-scratch-course) for detailed tutorials and examples.
"""

        readme_path = project_path / "README.md"
        with open(readme_path, "w") as f:
            f.write(readme_content)
        console.print(f"[green]✓[/green] Created README: {readme_path}")

        console.print("\n[green]🎉 Project setup completed successfully![/green]")
        console.print("\n[cyan]Next steps:[/cyan]")
        console.print("1. Copy .env.template to .env and update values")
        console.print("2. Run: adk-course validate")
        console.print("3. Run: adk-course init my-first-agent")

    except Exception as e:
        console.print(f"[red]❌ Project setup failed: {format_error_message(e)}[/red]")
        raise typer.Exit(1)


def interactive_setup() -> None:
    """Run interactive setup wizard."""
    console.print("\n[bold blue]🧙 ADK Course Setup Wizard[/bold blue]")

    # Get project information
    project_name = Prompt.ask("Project name", default="my-adk-project")

    project_path = Path.cwd() / project_name

    if project_path.exists():
        if not Confirm.ask(f"Directory {project_path} already exists. Continue?"):
            console.print("[yellow]Setup cancelled.[/yellow]")
            return

    # Get Google Cloud information
    console.print("\n[bold]Google Cloud Configuration[/bold]")
    project_id = Prompt.ask("Google Cloud Project ID")
    location = Prompt.ask("Google Cloud Location", default="us-central1")

    # Get agent information
    console.print("\n[bold]Default Agent Configuration[/bold]")
    agent_name = Prompt.ask("Default agent name", default="my-agent")
    agent_description = Prompt.ask("Agent description", default="My first ADK agent")

    try:
        # Set up project
        setup_project(project_path)

        # Update configuration with user values
        config = create_agent_config_template()
        config.update(
            {
                "name": agent_name,
                "description": agent_description,
                "project_id": project_id,
                "location": location,
            }
        )

        config_path = project_path / "configs" / "default-agent.yaml"
        save_config(config, config_path)

        # Create .env file
        env_content = f"""GOOGLE_CLOUD_PROJECT={project_id}
GOOGLE_CLOUD_LOCATION={location}
# GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

ADK_LOG_LEVEL=INFO
ADK_LOG_FORMAT=console
"""

        with open(project_path / ".env", "w") as f:
            f.write(env_content)

        console.print(
            f"\n[green]🎉 Project '{project_name}' created successfully![/green]"
        )
        console.print(f"\n[cyan]To get started:[/cyan]")
        console.print(f"1. cd {project_path}")
        console.print("2. Set up your Google Cloud credentials")
        console.print("3. Run: adk-course validate")

    except Exception as e:
        console.print(f"[red]❌ Setup failed: {format_error_message(e)}[/red]")
        raise typer.Exit(1)


def main() -> None:
    """Provide main entry point for setup CLI."""
    console.print("\n[bold blue]⚙️  ADK Course Setup[/bold blue]")

    # Ask what the user wants to do
    choices = [
        "Interactive setup wizard",
        "Set up project in current directory",
        "Cancel",
    ]

    console.print("\nWhat would you like to do?")
    for i, choice in enumerate(choices, 1):
        console.print(f"{i}. {choice}")

    while True:
        try:
            selection = int(Prompt.ask("Choose an option", default="1"))
            if 1 <= selection <= len(choices):
                break
            console.print("[red]Invalid selection. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a number.[/red]")

    if selection == 1:
        interactive_setup()
    elif selection == 2:
        setup_project()
    else:
        console.print("[yellow]Setup cancelled.[/yellow]")


if __name__ == "__main__":
    main()
