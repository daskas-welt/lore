"""Rich-based rendering for the TUI content pane."""

from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


console = Console()


def render_entry(entry) -> None:
    """Render a single LoreEntry with formatting."""
    title = Text()
    title.append(f"  {entry.type.upper()}  ", style="bold yellow")
    title.append("  ")
    title.append(entry.name, style="bold white")

    subtitle = ""
    if entry.tags:
        subtitle = " ".join(f"[dim green]#{tag}[/dim green]" for tag in entry.tags)

    md = Markdown(entry.content) if entry.content else Text("")

    panel = Panel(
        md,
        title=title,
        subtitle=subtitle if subtitle else None,
        subtitle_align="right",
        border_style="bright_cyan",
        padding=(1, 2),
    )

    console.print(panel)

    if entry.variants:
        console.print()
        for key, value in entry.variants.items():
            variant_panel = Panel(
                Markdown(value) if isinstance(value, str) else value,
                title=f"[bold magenta]{key.title()}[/bold magenta]",
                border_style="dim",
                padding=(0, 1),
            )
            console.print(variant_panel)


def render_list(title: str, items: list[dict], columns: list[str]) -> None:
    """Render a list of items as a Rich table."""
    table = Table(
        title=title, show_header=True, header_style="bold cyan", border_style="dim"
    )

    for col in columns:
        table.add_column(col, style="white")

    for item in items:
        row = []
        for col in columns:
            val = item.get(col.lower(), "")
            if isinstance(val, list):
                val = ", ".join(str(v) for v in val)
            row.append(str(val))
        table.add_row(*row)

    console.print(table)


def render_error(message: str) -> None:
    """Render an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def render_success(message: str) -> None:
    """Render a success message."""
    console.print(f"[bold green]+[/bold green] {message}")


def render_info(message: str) -> None:
    """Render an info message."""
    console.print(f"[dim]{message}[/dim]")
