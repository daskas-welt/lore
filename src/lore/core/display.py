"""Rich-based display rendering for Lore entries."""

from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme
from rich.text import Text


# Custom theme for consistent styling
THEME = Theme(
    {
        "lore.title": "bold cyan",
        "lore.subtitle": "dim italic",
        "lore.type": "bold yellow",
        "lore.tag": "dim green",
        "lore.name": "bold white",
        "lore.header": "bold magenta",
        "lore.accent": "bright_cyan",
        "lore.muted": "dim",
    }
)

console = Console(theme=THEME)


def render_entry(
    name: str,
    entry_type: str,
    tags: list[str],
    content: str,
    variants: Optional[dict] = None,
) -> None:
    """Render a lore entry with Rich formatting."""
    # Build title with type badge
    title = Text()
    title.append(f"  {entry_type.upper()}  ", style="lore.type")
    title.append("  ")
    title.append(name, style="lore.name")

    # Build subtitle with tags
    subtitle = ""
    if tags:
        subtitle = " ".join(f"[lore.tag]#{tag}[/lore.tag]" for tag in tags)

    # Render markdown content
    md = Markdown(content)

    # Create panel with content
    panel = Panel(
        md,
        title=title,
        subtitle=subtitle if subtitle else None,
        subtitle_align="right",
        border_style="lore.accent",
        padding=(1, 2),
    )

    console.print(panel)

    # Render variants if present
    if variants:
        console.print()
        for key, value in variants.items():
            variant_panel = Panel(
                Markdown(value),
                title=f"[lore.header]{key.title()}[/lore.header]",
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
        row = [item.get(col.lower(), "") for col in columns]
        table.add_row(*row)

    console.print(table)


def render_campaigns(campaigns: list[str], active: Optional[str] = None) -> None:
    """Render the list of campaigns."""
    table = Table(
        title="Campaigns",
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Name", style="white")
    table.add_column("Status", justify="center")

    for name in sorted(campaigns):
        status = "[green]* active[/green]" if name == active else "[dim]-[/dim]"
        style = "bold" if name == active else ""
        table.add_row(Text(name, style=style), status)

    console.print(table)


def render_scenes(scenes: list[dict], campaign_name: str) -> None:
    """Render the list of scenes."""
    table = Table(
        title=f"Scenes in {campaign_name}",
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )
    table.add_column("Name", style="white")
    table.add_column("Tags", style="dim green")

    for scene in scenes:
        name = scene.get("name", "")
        tags = ", ".join(scene.get("tags", []))
        table.add_row(name, tags)

    console.print(table)


def render_npcs(npcs: list[dict]) -> None:
    """Render the list of NPCs."""
    table = Table(
        title="NPCs", show_header=True, header_style="bold cyan", border_style="dim"
    )
    table.add_column("Name", style="white")
    table.add_column("Role", style="yellow")
    table.add_column("Tags", style="dim green")

    for npc in npcs:
        name = npc.get("name", "")
        role = npc.get("role", "")
        tags = ", ".join(npc.get("tags", []))
        table.add_row(name, role, tags)

    console.print(table)


def render_objects(objects: list[dict]) -> None:
    """Render the list of objects."""
    table = Table(
        title="Objects", show_header=True, header_style="bold cyan", border_style="dim"
    )
    table.add_column("Name", style="white")
    table.add_column("Category", style="yellow")
    table.add_column("Tags", style="dim green")

    for obj in objects:
        name = obj.get("name", "")
        category = obj.get("category", "")
        tags = ", ".join(obj.get("tags", []))
        table.add_row(name, category, tags)

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
