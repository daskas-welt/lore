"""NPC and Object commands."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from ..core.config import require_active_campaign_path, get_active_campaign_path
from ..core.loader import load_campaign_entries, find_entry_by_name
from ..core.display import format_entry_header, format_entry_content

console = Console()


def show_npc(name: str, campaign: Optional[str] = None) -> None:
    """Show an NPC by name."""
    campaign_path = _get_campaign_path(campaign)
    entry = find_entry_by_name(campaign_path, name, entry_type="npc")

    if entry is None:
        console.print(f"[red]NPC '{name}' not found[/red]")
        raise typer.Exit(1)

    header = format_entry_header(entry.name, entry.type, entry.tags)
    console.print(header)
    console.print()

    content = format_entry_content(entry.content, entry.variants)
    console.print(content)


def list_npcs(role: Optional[str] = None) -> None:
    """List all NPCs in the active campaign."""
    campaign_path = require_active_campaign_path()
    entries = load_campaign_entries(campaign_path, entry_type="npc")

    if role:
        entries = [
            e for e in entries if e.frontmatter.get("role", "").lower() == role.lower()
        ]

    if not entries:
        console.print("[yellow]No NPCs found.[/yellow]")
        return

    console.print("[bold]NPCs:[/bold]")
    for entry in sorted(entries, key=lambda e: e.name):
        role_str = (
            f" ({entry.frontmatter.get('role', '')})"
            if entry.frontmatter.get("role")
            else ""
        )
        tags = f" [{', '.join(entry.tags)}]" if entry.tags else ""
        console.print(f"  • {entry.name}{role_str}{tags}")


def show_object(name: str, campaign: Optional[str] = None) -> None:
    """Show an object by name."""
    campaign_path = _get_campaign_path(campaign)
    entry = find_entry_by_name(campaign_path, name, entry_type="object")

    if entry is None:
        console.print(f"[red]Object '{name}' not found[/red]")
        raise typer.Exit(1)

    header = format_entry_header(entry.name, entry.type, entry.tags)
    console.print(header)
    console.print()

    content = format_entry_content(entry.content, entry.variants)
    console.print(content)


def list_objects(category: Optional[str] = None) -> None:
    """List all objects in the active campaign."""
    campaign_path = require_active_campaign_path()
    entries = load_campaign_entries(campaign_path, entry_type="object")

    if category:
        entries = [
            e
            for e in entries
            if e.frontmatter.get("category", "").lower() == category.lower()
        ]

    if not entries:
        console.print("[yellow]No objects found.[/yellow]")
        return

    console.print("[bold]Objects:[/bold]")
    for entry in sorted(entries, key=lambda e: e.name):
        cat_str = (
            f" ({entry.frontmatter.get('category', '')})"
            if entry.frontmatter.get("category")
            else ""
        )
        tags = f" [{', '.join(entry.tags)}]" if entry.tags else ""
        console.print(f"  • {entry.name}{cat_str}{tags}")


def _get_campaign_path(campaign: Optional[str] = None) -> Path:
    """Get campaign path from name or active campaign."""
    from ..core.config import get_campaigns_path

    if campaign:
        campaigns_dir = get_campaigns_path()
        path = campaigns_dir / campaign
        if not path.exists():
            console.print(f"[red]Campaign '{campaign}' not found[/red]")
            raise typer.Exit(1)
        return path

    return require_active_campaign_path()
