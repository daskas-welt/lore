"""Campaign management commands."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from ..core.config import (
    load_config,
    save_config,
    set_active_campaign,
    get_campaigns_path,
    get_active_campaign_path,
    list_campaigns,
)

console = Console()


def list_campaigns_cmd() -> None:
    """List all available campaigns."""
    campaigns = list_campaigns()
    config = load_config()

    if not campaigns:
        console.print("[yellow]No campaigns found.[/yellow]")
        console.print("Use 'lore init <name>' to create one.")
        return

    console.print("[bold]Campaigns:[/bold]")
    for name in sorted(campaigns):
        if name == config.active_campaign:
            console.print(f"  * {name} [green](active)[/green]")
        else:
            console.print(f"    {name}")


def use_campaign_cmd(name: str) -> None:
    """Switch to a different campaign."""
    campaigns = list_campaigns()

    if name not in campaigns:
        console.print(f"[red]Campaign '{name}' not found.[/red]")
        console.print(f"Available: {', '.join(campaigns)}")
        raise typer.Exit(1)

    set_active_campaign(name)
    console.print(f"[green]Switched to campaign '{name}'[/green]")


def init_campaign_cmd(name: str) -> None:
    """Create a new campaign with directory structure."""
    campaigns_dir = get_campaigns_path()
    campaign_path = campaigns_dir / name

    if campaign_path.exists():
        console.print(f"[yellow]Campaign '{name}' already exists.[/yellow]")
        return

    # Create directory structure
    for subdir in ["areas", "npcs", "groups", "objects"]:
        (campaign_path / subdir).mkdir(parents=True, exist_ok=True)

    # Set as active campaign
    set_active_campaign(name)

    console.print(f"[green]Created campaign '{name}'[/green]")
    console.print(f"Location: {campaign_path}")
    console.print("Added directories: areas/, npcs/, groups/, objects/")
    console.print("Set as active campaign.")


def list_scenes_cmd() -> None:
    """List all scenes in the active campaign."""
    from ..core.loader import load_campaign_entries

    campaign_path = get_active_campaign_path()
    if campaign_path is None:
        console.print("[red]No active campaign. Use 'lore use <name>' to switch.[/red]")
        raise typer.Exit(1)

    entries = load_campaign_entries(campaign_path, entry_type="area")

    if not entries:
        console.print("[yellow]No scenes found in this campaign.[/yellow]")
        return

    console.print(f"[bold]Scenes in {campaign_path.name}:[/bold]")
    for entry in sorted(entries, key=lambda e: e.name):
        tags = f" [{', '.join(entry.tags)}]" if entry.tags else ""
        console.print(f"  • {entry.name}{tags}")
