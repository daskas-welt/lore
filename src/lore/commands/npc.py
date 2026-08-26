"""NPC and Object commands."""

from typing import Optional

import typer

from ..core.loader import load_campaign_entries, find_entry_by_name
from ..core.display import render_entry, render_npcs, render_objects, render_error
from ._util import get_campaign_path


def show_npc(name: str, campaign: Optional[str] = None) -> None:
    """Show an NPC by name."""
    campaign_path = get_campaign_path(campaign)
    entry = find_entry_by_name(campaign_path, name, entry_type="npc")

    if entry is None:
        render_error(f"NPC '{name}' not found")
        raise typer.Exit(1)

    render_entry(entry.name, entry.type, entry.tags, entry.content, entry.variants)


def list_npcs(role: Optional[str] = None) -> None:
    """List all NPCs in the active campaign."""
    from ..core.config import require_active_campaign_path

    campaign_path = require_active_campaign_path()
    entries = load_campaign_entries(campaign_path, entry_type="npc")

    if role:
        entries = [
            e for e in entries if e.frontmatter.get("role", "").lower() == role.lower()
        ]

    if not entries:
        render_error("No NPCs found.")
        return

    npcs = [
        {
            "name": e.name,
            "role": e.frontmatter.get("role", ""),
            "tags": e.tags,
        }
        for e in sorted(entries, key=lambda e: e.name)
    ]

    render_npcs(npcs)


def show_object(name: str, campaign: Optional[str] = None) -> None:
    """Show an object by name."""
    campaign_path = get_campaign_path(campaign)
    entry = find_entry_by_name(campaign_path, name, entry_type="object")

    if entry is None:
        render_error(f"Object '{name}' not found")
        raise typer.Exit(1)

    render_entry(entry.name, entry.type, entry.tags, entry.content, entry.variants)


def list_objects(category: Optional[str] = None) -> None:
    """List all objects in the active campaign."""
    from ..core.config import require_active_campaign_path

    campaign_path = require_active_campaign_path()
    entries = load_campaign_entries(campaign_path, entry_type="object")

    if category:
        entries = [
            e
            for e in entries
            if e.frontmatter.get("category", "").lower() == category.lower()
        ]

    if not entries:
        render_error("No objects found.")
        return

    objects = [
        {
            "name": e.name,
            "category": e.frontmatter.get("category", ""),
            "tags": e.tags,
        }
        for e in sorted(entries, key=lambda e: e.name)
    ]

    render_objects(objects)
