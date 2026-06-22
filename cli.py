#!/usr/bin/env python3
"""
cli.py
Multi-turn CLI interface for the vehicle sales agent.
Usage:  python cli.py
        python cli.py --model gpt-4o
"""

import argparse
import os
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

load_dotenv()  # reads OPENAI_API_KEY from .env if present

console = Console()

BANNER = """
[bold cyan]╔═══════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║   🚗  Craigslist Vehicle Sales Assistant       ║[/bold cyan]
[bold cyan]║   Powered by GPT + live inventory search       ║[/bold cyan]
[bold cyan]╚═══════════════════════════════════════════════╝[/bold cyan]

Type your question or request. Commands:
  [bold]/reset[/bold]  – start a new conversation
  [bold]/quit[/bold]   – exit
"""

EXAMPLES = [
    "Do you have any Honda Civics under $15,000?",
    "Show me trucks from 2015 or newer in good condition",
    "What's the average price of a used Toyota Tacoma?",
    "I'm looking for a blue Ford F-150 with 8 cylinders",
    "Find me something under $5,000 in California",
]


def print_examples() -> None:
    console.print("\n[dim]Example questions you can ask:[/dim]")
    for i, ex in enumerate(EXAMPLES, 1):
        console.print(f"  [dim]{i}.[/dim] {ex}")
    console.print()


def main(model: str = "gpt-4o-mini") -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print(
            "[bold red]Error:[/bold red] OPENAI_API_KEY not set.\n"
            "Create a [bold].env[/bold] file with:  OPENAI_API_KEY=sk-..."
        )
        sys.exit(1)

    # Lazy import so missing DB doesn't crash before we print the banner
    try:
        from agent.agent import SalesAgent
    except FileNotFoundError as e:
        console.print(f"[bold red]Setup error:[/bold red] {e}")
        sys.exit(1)

    agent = SalesAgent(model=model, api_key=api_key)

    console.print(BANNER)
    print_examples()

    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/quit", "/exit", "quit", "exit"):
            console.print("[dim]Goodbye![/dim]")
            break

        if user_input.lower() == "/reset":
            agent.reset()
            console.print("[dim]Conversation reset.[/dim]\n")
            continue

        # Show a spinner while the agent thinks
        with console.status("[dim]Searching inventory…[/dim]", spinner="dots"):
            try:
                response = agent.chat(user_input)
            except Exception as exc:
                console.print(f"[bold red]Error:[/bold red] {exc}")
                continue

        console.print(
            Panel(
                Markdown(response),
                title="[bold blue]Sales Assistant[/bold blue]",
                border_style="blue",
                padding=(1, 2),
            )
        )
        console.print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vehicle Sales Agent CLI")
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model to use (default: gpt-4o-mini)",
    )
    args = parser.parse_args()
    main(model=args.model)
