"""Campaign management commands."""

import typer

from ..core.config import (
    load_config,
    set_active_campaign,
    get_campaigns_path,
    get_active_campaign_path,
    list_campaigns,
)
from ..core.display import (
    render_campaigns,
    render_scenes,
    render_error,
    render_success,
    render_info,
)


def list_campaigns_cmd() -> None:
    """List all available campaigns."""
    campaigns = list_campaigns()
    config = load_config()

    if not campaigns:
        render_info("No campaigns found. Use 'lore init <name>' to create one.")
        return

    render_campaigns(campaigns, config.active_campaign)


def use_campaign_cmd(name: str) -> None:
    """Switch to a different campaign."""
    campaigns = list_campaigns()

    if name not in campaigns:
        render_error(f"Campaign '{name}' not found. Available: {', '.join(campaigns)}")
        raise typer.Exit(1)

    set_active_campaign(name)
    render_success(f"Switched to campaign '{name}'")


def init_campaign_cmd(name: str) -> None:
    """Create a new campaign with directory structure."""
    campaigns_dir = get_campaigns_path()
    campaign_path = campaigns_dir / name

    if campaign_path.exists():
        render_info(f"Campaign '{name}' already exists.")
        return

    # Create directory structure
    for subdir in ["areas", "npcs", "groups", "objects"]:
        (campaign_path / subdir).mkdir(parents=True, exist_ok=True)

    # Set as active campaign
    set_active_campaign(name)

    render_success(f"Created campaign '{name}'")
    render_info(f"Location: {campaign_path}")
    render_info("Added: areas/, npcs/, groups/, objects/")


def list_scenes_cmd() -> None:
    """List all scenes in the active campaign."""
    from ..core.loader import load_campaign_entries

    campaign_path = get_active_campaign_path()
    if campaign_path is None:
        render_error("No active campaign. Use 'lore use <name>' to switch.")
        raise typer.Exit(1)

    entries = load_campaign_entries(campaign_path, entry_type="area")

    if not entries:
        render_info("No scenes found in this campaign.")
        return

    scenes = [
        {"name": e.name, "tags": e.tags} for e in sorted(entries, key=lambda e: e.name)
    ]

    render_scenes(scenes, campaign_path.name)
