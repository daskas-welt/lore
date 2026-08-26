"""Display command for lore entries."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from ..core.config import require_active_campaign_path, get_active_campaign_path
from ..core.loader import (
    load_entries_from_dir,
    find_entry_by_name,
    find_file_by_substring,
)
from ..core.display import (
    format_entry_header,
    format_entry_content,
    render_markdown_to_ansi,
)

console = Console()


def display_entry(
    name: str,
    campaign_path: Optional[Path] = None,
    entry_type: Optional[str] = None,
    raw: bool = False,
) -> None:
    """Display a lore entry by name."""
    if campaign_path is None:
        campaign_path = require_active_campaign_path()

    entry = find_entry_by_name(campaign_path, name, entry_type)

    if entry is None:
        console.print(f"[red]No lore found matching '{name}'[/red]")
        raise typer.Exit(1)

    if raw:
        console.print(entry.content)
    else:
        header = format_entry_header(entry.name, entry.type, entry.tags)
        console.print(header)
        console.print()

        content = format_entry_content(entry.content, entry.variants)
        console.print(content)


def display_scene(name: str, campaign: Optional[str] = None) -> None:
    """Display a scene (area) entry."""
    campaign_path = _get_campaign_path(campaign)
    display_entry(name, campaign_path, entry_type="area")


def display_npc(name: str, campaign: Optional[str] = None) -> None:
    """Display an NPC entry."""
    campaign_path = _get_campaign_path(campaign)
    display_entry(name, campaign_path, entry_type="npc")


def display_object(name: str, campaign: Optional[str] = None) -> None:
    """Display an object entry."""
    campaign_path = _get_campaign_path(campaign)
    display_entry(name, campaign_path, entry_type="object")


def _get_campaign_path(campaign: Optional[str] = None) -> Path:
    """Get campaign path from name or active campaign."""
    from ..core.config import get_campaigns_path, load_config

    if campaign:
        campaigns_dir = get_campaigns_path()
        path = campaigns_dir / campaign
        if not path.exists():
            console.print(f"[red]Campaign '{campaign}' not found[/red]")
            raise typer.Exit(1)
        return path

    return require_active_campaign_path()
