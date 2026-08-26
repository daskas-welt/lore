"""Shared utilities for commands."""

from pathlib import Path
from typing import Optional

from rich.console import Console

from ..core.config import get_campaigns_path, require_active_campaign_path

console = Console()


def get_campaign_path(campaign: Optional[str] = None) -> Path:
    """Get campaign path from name or active campaign."""
    if campaign:
        campaigns_dir = get_campaigns_path()
        path = campaigns_dir / campaign
        if not path.exists():
            console.print(f"[red]Campaign '{campaign}' not found[/red]")
            raise SystemExit(1)
        return path

    return require_active_campaign_path()
