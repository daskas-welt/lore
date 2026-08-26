"""Frontmatter parsing and entry loading."""

from pathlib import Path
from typing import Optional

import frontmatter
import yaml

from .models import LoreEntry
from .config import get_active_campaign_path, get_campaigns_path


def parse_file(filepath: Path) -> Optional[LoreEntry]:
    """Parse a YAML or Markdown file with frontmatter into a LoreEntry."""
    if not filepath.exists():
        return None

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return None

    ext = filepath.suffix.lower()

    try:
        if ext == ".md":
            return _parse_markdown(filepath, content)
        elif ext in (".yaml", ".yml"):
            return _parse_yaml(filepath, content)
        elif ext == ".json":
            return _parse_json(filepath, content)
    except (ValueError, KeyError):
        return None

    return None


def _parse_markdown(filepath: Path, content: str) -> Optional[LoreEntry]:
    """Parse markdown file with YAML frontmatter."""
    try:
        post = frontmatter.loads(content)
    except Exception:
        return None

    fm = dict(post.metadata)
    body = post.content

    name = fm.get("name") or fm.get("title") or filepath.stem
    entry_type = fm.get("type", "area")
    tags = fm.get("tags", [])

    # Check for variants in frontmatter
    variants = {}
    if "variants" in fm and isinstance(fm["variants"], dict):
        variants = fm["variants"]

    return LoreEntry(
        name=name,
        type=entry_type,
        tags=tags,
        path=filepath,
        content=body.strip(),
        frontmatter=fm,
        variants=variants,
    )


def _parse_yaml(filepath: Path, content: str) -> Optional[LoreEntry]:
    """Parse YAML file."""
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError:
        return None

    if not isinstance(data, dict):
        return None

    name = data.get("name") or data.get("title") or filepath.stem
    entry_type = data.get("type", "area")
    tags = data.get("tags", [])
    description = data.get("description", "")
    variants = data.get("variants", {})

    return LoreEntry(
        name=name,
        type=entry_type,
        tags=tags,
        path=filepath,
        content=description.strip() if isinstance(description, str) else "",
        frontmatter=data,
        variants=variants if isinstance(variants, dict) else {},
    )


def _parse_json(filepath: Path, content: str) -> Optional[LoreEntry]:
    """Parse JSON file."""
    try:
        import json

        data = json.loads(content)
    except Exception:
        return None

    if not isinstance(data, dict):
        return None

    name = data.get("name") or data.get("title") or filepath.stem
    entry_type = data.get("type", "area")
    tags = data.get("tags", [])
    description = data.get("description", "")
    variants = data.get("variants", {})

    return LoreEntry(
        name=name,
        type=entry_type,
        tags=tags,
        path=filepath,
        content=description.strip() if isinstance(description, str) else "",
        frontmatter=data,
        variants=variants if isinstance(variants, dict) else {},
    )


def load_entries_from_dir(directory: Path) -> list[LoreEntry]:
    """Load all valid entries from a directory."""
    entries = []

    if not directory.exists():
        return entries

    for file in sorted(directory.iterdir()):
        if file.is_file() and file.suffix.lower() in (".md", ".yaml", ".yml", ".json"):
            entry = parse_file(file)
            if entry is not None:
                entries.append(entry)

    return entries


def load_campaign_entries(
    campaign_path: Path, entry_type: Optional[str] = None
) -> list[LoreEntry]:
    """Load all entries from a campaign, optionally filtered by type."""
    entries = []

    # Load from subdirectories: areas/, npcs/, groups/, objects/
    type_dirs = {
        "area": "areas",
        "npc": "npcs",
        "group": "groups",
        "object": "objects",
    }

    if entry_type:
        dirs_to_load = [campaign_path / type_dirs.get(entry_type, entry_type + "s")]
    else:
        dirs_to_load = [campaign_path / d for d in type_dirs.values()]

    for directory in dirs_to_load:
        if directory.exists():
            entries.extend(load_entries_from_dir(directory))

    # Also load from root directory (for backward compatibility)
    if entry_type is None:
        entries.extend(load_entries_from_dir(campaign_path))

    return entries


def find_entry_by_name(
    campaign_path: Path,
    query: str,
    entry_type: Optional[str] = None,
) -> Optional[LoreEntry]:
    """Find an entry by name (exact match, then substring, then filename)."""
    entries = load_campaign_entries(campaign_path, entry_type)
    q = query.lower()

    # Exact name match
    for entry in entries:
        if entry.name.lower() == q:
            return entry

    # Substring match in name
    for entry in entries:
        if q in entry.name.lower():
            return entry

    # Filename match
    for entry in entries:
        if q in entry.path.stem.lower():
            return entry

    return None


def find_file_by_substring(directory: Path, query: str) -> Optional[Path]:
    """Find a file by name substring (filename or frontmatter name/title)."""
    if not directory.exists():
        return None

    q = query.lower()

    # First try filename match
    for file in directory.iterdir():
        if file.is_file() and file.suffix.lower() in (".md", ".yaml", ".yml", ".json"):
            base = file.stem.lower()
            if q in base:
                return file

    # Then try frontmatter name/title match
    for file in directory.iterdir():
        if file.is_file() and file.suffix.lower() in (".md", ".yaml", ".yml", ".json"):
            entry = parse_file(file)
            if entry is not None:
                if q in entry.name.lower():
                    return file

    return None
