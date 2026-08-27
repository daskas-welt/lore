"""Configuration and path management for Lore."""

import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".lore"
CONTENT_DIR = CONFIG_DIR / "content"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_content_path() -> Path:
    """Get the path to the content directory."""
    return CONTENT_DIR


def ensure_content_dir() -> None:
    """Create the content directory and subdirectories if they don't exist."""
    for subdir in ["areas", "npcs", "groups", "objects"]:
        (CONTENT_DIR / subdir).mkdir(parents=True, exist_ok=True)


def get_theme() -> str:
    """End-user theme preference — persisted in ~/.lore/config.json (light default)."""
    if not CONFIG_FILE.exists():
        return "light"
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        v = data.get("theme", "light")
        return v if v in ("light", "dark") else "light"
    except Exception:
        return "light"


def set_theme(mode: str) -> None:
    """Persist end-user theme preference."""
    if mode not in ("light", "dark"):
        mode = "light"
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data["theme"] = mode
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
