"""Configuration management for ~/.lore/config.json."""

import json
from pathlib import Path
from typing import Optional

import typer

from .models import Config


CONFIG_DIR = Path.home() / ".lore"
CONFIG_FILE = CONFIG_DIR / "config.json"
CAMPAIGNS_DIR = CONFIG_DIR / "campaigns"


def get_config_path() -> Path:
    """Get the path to the config file."""
    return CONFIG_FILE


def get_campaigns_path() -> Path:
    """Get the path to the campaigns directory."""
    return CAMPAIGNS_DIR


def load_config() -> Config:
    """Load config from ~/.lore/config.json, or return defaults."""
    if not CONFIG_FILE.exists():
        return Config()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Config(
            active_campaign=data.get("activeCampaign"),
            campaigns_path=data.get("campaignsPath", ""),
            version=data.get("version", "2.0.0"),
            preferences=data.get("preferences", {}),
        )
    except (json.JSONDecodeError, KeyError):
        return Config()


def save_config(config: Config) -> None:
    """Save config to ~/.lore/config.json."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        "activeCampaign": config.active_campaign,
        "campaignsPath": config.campaigns_path,
        "version": config.version,
        "preferences": config.preferences,
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_active_campaign_path() -> Optional[Path]:
    """Get the path to the active campaign directory."""
    config = load_config()
    if config.active_campaign is None:
        return None

    campaign_path = CAMPAIGNS_DIR / config.active_campaign
    if campaign_path.exists() and campaign_path.is_dir():
        return campaign_path

    return None


def require_active_campaign_path() -> Path:
    """Get the active campaign path, or raise an error if none is set."""
    path = get_active_campaign_path()
    if path is None:
        raise typer.Exit(
            1, message="No active campaign. Use 'lore use <campaign>' to set one."
        )
    return path


def set_active_campaign(name: str) -> None:
    """Set the active campaign in config."""
    config = load_config()
    config.active_campaign = name
    save_config(config)


def list_campaigns() -> list[str]:
    """List all available campaigns."""
    if not CAMPAIGNS_DIR.exists():
        return []

    return [
        d.name
        for d in CAMPAIGNS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ]
