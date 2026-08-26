"""Display command for lore entries."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from ..core.config import require_active_campaign_path
from ..core.loader import find_entry_by_name
from ..core.display import format_entry_header, format_entry_content

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
