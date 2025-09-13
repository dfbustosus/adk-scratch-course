"""Command-line interface for the ADK Course package."""

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .core import AgentConfig, BasicAgent
from .exceptions import ADKError
from .utils import (
    create_agent_config_template,
    format_error_message,
    load_config,
    save_config,
    setup_logging,
    validate_environment,
)

app = typer.Typer(
    name="adk-course",
    help="ADK Course CLI - Tools for working with Google Development Kit agents",
)
console = Console()


@app.command()
def validate() -> None:
    """Validate the development environment."""
    console.print("\n[bold blue]🔍 Validating Environment[/bold blue]")

    try:
        status = validate_environment()

        # Display Python information
        console.print(f"\n[green]✓[/green] Python: {status['python_version']}")
        console.print(f"[green]✓[/green] Python Path: {status['python_path']}")

        # Display environment variables
        if status["environment_variables"]:
            table = Table(title="Environment Variables")
            table.add_column("Variable", style="cyan")
            table.add_column("Status", style="green")

            for var, value in status["environment_variables"].items():
                table.add_row(var, value)

            console.print(table)

        # Display Google Cloud status
        if status["google_cloud_setup"]:
            project = status.get("google_cloud_project", "unknown project")
            console.print(f"\n[green]✓[/green] Google Cloud: Connected to {project}")
        else:
            console.print("\n[yellow]⚠[/yellow] Google Cloud: Not configured")

        # Display warnings
        if status["warnings"]:
            console.print("\n[bold yellow]Warnings:[/bold yellow]")
            for warning in status["warnings"]:
                console.print(f"[yellow]⚠[/yellow] {warning}")

        console.print(
            "\n[green]✅ Environment validation completed successfully![/green]"
        )

    except Exception as e:
        error_msg = format_error_message(e)
        console.print(f"\n[red]❌ Environment validation failed: {error_msg}[/red]")
        raise typer.Exit(1)


@app.command()
def init(
    name: str = typer.Argument(..., help="Agent name"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output directory"
    ),
) -> None:
    """Initialize a new agent configuration."""
    console.print(f"\n[bold blue]🚀 Initializing agent: {name}[/bold blue]")

    try:
        # Set default output directory
        if output is None:
            output = Path.cwd() / "agents" / name

        # Create directory
        output.mkdir(parents=True, exist_ok=True)

        # Create configuration
        config = create_agent_config_template()
        config["name"] = name
        config["description"] = f"Agent configuration for {name}"

        config_path = output / "config.yaml"
        save_config(config, config_path)

        # Create example files
        examples_dir = output / "examples"
        examples_dir.mkdir(exist_ok=True)

        example_code = f'''"""
Example usage of the {name} agent.
"""
import asyncio
from pathlib import Path
from adk_course import AgentConfig, BasicAgent

async def main():
    """Example agent usage."""
    # Load configuration
    config_path = Path(__file__).parent / "config.yaml"
    config_dict = load_config(config_path)
    config = AgentConfig(**config_dict)

    # Create agent
    agent = BasicAgent(config)

    # Send a message
    response = await agent.process_message("Hello, agent!")
    print(f"Agent response: {{response}}")

    # Get status
    status = agent.get_status()
    print(f"Agent status: {{status}}")

if __name__ == "__main__":
    asyncio.run(main())
'''

        with open(examples_dir / f"{name}_example.py", "w") as f:
            f.write(example_code)

        console.print(f"[green]✅ Agent '{name}' initialized successfully![/green]")
        console.print(f"[cyan]📁 Configuration saved to: {config_path}[/cyan]")
        example_file = examples_dir / f"{name}_example.py"
        console.print(f"[cyan]📄 Example code saved to: {example_file}[/cyan]")

    except Exception as e:
        error_msg = format_error_message(e)
        console.print(f"[red]❌ Failed to initialize agent: {error_msg}[/red]")
        raise typer.Exit(1)


@app.command()
def chat(
    config_file: Path = typer.Option(
        Path("config.yaml"), "--config", "-c", help="Agent configuration file"
    ),
) -> None:
    """Start an interactive chat session with an agent."""
    console.print("\n[bold blue]💬 Starting Interactive Chat[/bold blue]")

    try:
        # Load configuration
        config_dict = load_config(config_file)
        config = AgentConfig(**config_dict)

        console.print(f"[green]✅ Loaded agent: {config.name}[/green]")
        console.print(f"[cyan]📝 Description: {config.description}[/cyan]")
        console.print("\n[yellow]Type 'quit' or 'exit' to end the session[/yellow]")
        console.print("[yellow]Type 'status' to see agent status[/yellow]")
        console.print("[yellow]Type 'history' to see conversation history[/yellow]\n")

        # Create agent
        agent = BasicAgent(config)

        while True:
            try:
                user_input = typer.prompt("You")

                if user_input.lower() in ["quit", "exit"]:
                    console.print("\n[blue]👋 Goodbye![/blue]")
                    break

                if user_input.lower() == "status":
                    status = agent.get_status()
                    table = Table(title="Agent Status")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value", style="green")

                    for key, value in status.items():
                        if key != "config":  # Skip config display for brevity
                            table.add_row(str(key), str(value))

                    console.print(table)
                    continue

                if user_input.lower() == "history":
                    history = agent.get_history(limit=10)
                    if history:
                        console.print("\n[bold]Recent Conversation History:[/bold]")
                        for msg in history:
                            role_color = "blue" if msg.role == "user" else "green"
                            role_title = msg.role.title()
                            msg_text = (
                                f"[{role_color}]{role_title}:[/{role_color}] "
                                f"{msg.content}"
                            )
                            console.print(msg_text)
                    else:
                        console.print(
                            "[yellow]No conversation history available[/yellow]"
                        )
                    continue

                # Process message
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    progress.add_task(description="Thinking...", total=None)
                    response = asyncio.run(agent.process_message(user_input))

                console.print(f"[green]Agent:[/green] {response}")

            except KeyboardInterrupt:
                console.print("\n\n[blue]👋 Chat session interrupted. Goodbye![/blue]")
                break
            except Exception as e:
                console.print(f"[red]❌ Error: {format_error_message(e)}[/red]")

    except Exception as e:
        console.print(f"[red]❌ Failed to start chat: {format_error_message(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def test(
    config_file: Path = typer.Option(
        Path("config.yaml"), "--config", "-c", help="Agent configuration file"
    ),
    message: str = typer.Option(
        "Hello, agent!", "--message", "-m", help="Test message"
    ),
) -> None:
    """Test an agent with a simple message."""
    console.print(
        f"\n[bold blue]🧪 Testing agent with message: '{message}'[/bold blue]"
    )

    try:
        # Load configuration
        config_dict = load_config(config_file)
        config = AgentConfig(**config_dict)

        # Create agent
        agent = BasicAgent(config)

        # Send test message
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Processing message...", total=None)
            response = asyncio.run(agent.process_message(message))

        # Display results
        panel = Panel(
            f"[green]Response:[/green] {response}",
            title=f"Agent: {config.name}",
            title_align="left",
        )
        console.print(panel)

        # Display status
        status = agent.get_status()
        console.print(
            f"\n[cyan]📊 Messages processed: {status['message_count']}[/cyan]"
        )

    except Exception as e:
        console.print(f"[red]❌ Test failed: {format_error_message(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """Show version information."""
    from . import __author__, __version__

    console.print(f"\n[bold blue]ADK Course[/bold blue]")
    console.print(f"Version: [green]{__version__}[/green]")
    console.print(f"Author: [cyan]{__author__}[/cyan]")
    homepage_url = "https://github.com/dfbustosus/adk-scratch-course"
    console.print(f"Homepage: [link]{homepage_url}[/link]")


def main() -> None:
    """Main entry point for the CLI."""
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
