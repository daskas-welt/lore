"""Display command for lore entries."""

from typing import Optional

import typer

from ..core.config import require_active_campaign_path
from ..core.loader import find_entry_by_name
from ..core.display import render_entry, render_error


def display_entry(
    name: str,
    campaign_path: Optional[str] = None,
    entry_type: Optional[str] = None,
    raw: bool = False,
) -> None:
    """Display a lore entry by name."""
    from pathlib import Path

    if campaign_path:
        path = Path(campaign_path)
    else:
        path = require_active_campaign_path()

    entry = find_entry_by_name(path, name, entry_type)

    if entry is None:
        render_error(f"No lore found matching '{name}'")
        raise typer.Exit(1)

    if raw:
        from ..core.display import console

        console.print(entry.content)
    else:
        render_entry(entry.name, entry.type, entry.tags, entry.content, entry.variants)
