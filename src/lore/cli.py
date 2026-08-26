"""Lore CLI - A fast CLI tool for Dungeon Masters to retrieve read-aloud descriptions."""

from typing import Optional

import typer
from rich.console import Console

from . import __version__
from .commands.display import display_entry, display_scene, display_npc, display_object
from .commands.campaign import (
    list_campaigns_cmd,
    use_campaign_cmd,
    init_campaign_cmd,
    list_scenes_cmd,
)
from .commands.npc import show_npc, list_npcs, show_object, list_objects

app = typer.Typer(
    name="lore",
    help="A fast CLI tool for Dungeon Masters to retrieve read-aloud descriptions.",
    no_args_is_help=True,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"Lore version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    """Lore - A fast CLI tool for Dungeon Masters to retrieve read-aloud descriptions."""
    pass


@app.command()
def display(
    name: str = typer.Argument(..., help="Name of the lore entry to display"),
    campaign: Optional[str] = typer.Option(
        None, "--campaign", "-c", help="Campaign name"
    ),
    entry_type: Optional[str] = typer.Option(
        None, "--type", "-t", help="Entry type (area, npc, group, object)"
    ),
    raw: bool = typer.Option(
        False, "--raw", "-r", help="Display raw markdown without formatting"
    ),
):
    """Display a lore entry by name."""
    from .core.config import get_active_campaign_path, require_active_campaign_path

    if campaign:
        from .core.config import get_campaigns_path

        campaign_path = get_campaigns_path() / campaign
        if not campaign_path.exists():
            console.print(f"[red]Campaign '{campaign}' not found[/red]")
            raise typer.Exit(1)
    else:
        campaign_path = require_active_campaign_path()

    display_entry(name, campaign_path, entry_type=entry_type, raw=raw)


@app.command()
def campaigns():
    """List all available campaigns."""
    list_campaigns_cmd()


@app.command()
def use(
    name: str = typer.Argument(..., help="Campaign name to switch to"),
):
    """Switch to a different campaign."""
    use_campaign_cmd(name)


@app.command()
def init(
    name: str = typer.Argument(..., help="Name for the new campaign"),
):
    """Create a new campaign with directory structure."""
    init_campaign_cmd(name)


@app.command()
def scenes():
    """List all scenes in the active campaign."""
    list_scenes_cmd()


@app.command()
def npc(
    name: str = typer.Argument(..., help="NPC name to display"),
    campaign: Optional[str] = typer.Option(
        None, "--campaign", "-c", help="Campaign name"
    ),
):
    """Show an NPC by name."""
    show_npc(name, campaign)


@app.command()
def npcs(
    role: Optional[str] = typer.Option(None, "--role", "-r", help="Filter by role"),
):
    """List all NPCs in the active campaign."""
    list_npcs(role)


@app.command()
def object(
    name: str = typer.Argument(..., help="Object name to display"),
    campaign: Optional[str] = typer.Option(
        None, "--campaign", "-c", help="Campaign name"
    ),
):
    """Show an object by name."""
    show_object(name, campaign)


@app.command()
def objects(
    category: Optional[str] = typer.Option(
        None, "--category", "-c", help="Filter by category"
    ),
):
    """List all objects in the active campaign."""
    list_objects(category)


if __name__ == "__main__":
    app()
