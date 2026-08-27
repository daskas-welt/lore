"""File parsing and entry loading."""

from pathlib import Path
from typing import Optional

import frontmatter
import yaml

from .models import LoreEntry


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

    name = fm.get("name") or fm.get("title")
    entry_type = fm.get("type", "area")
    tags = fm.get("tags", [])

    # Extract variants from frontmatter
    variants = {}
    if "variants" in fm and isinstance(fm["variants"], dict):
        variants = fm["variants"]

    # If no name in frontmatter, try to extract from first heading
    if not name:
        for line in body.split("\n"):
            stripped = line.strip()
            if stripped.startswith("# "):
                name = stripped[2:].strip()
                break

    # Fallback to filename stem
    if not name:
        name = filepath.stem

    return LoreEntry(
        name=str(name),
        type=str(entry_type),
        tags=list(tags),
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
        name=str(name),
        type=str(entry_type),
        tags=list(tags),
        path=filepath,
        content=str(description).strip() if isinstance(description, str) else "",
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
        name=str(name),
        type=str(entry_type),
        tags=list(tags),
        path=filepath,
        content=str(description).strip() if isinstance(description, str) else "",
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


def load_all_entries(
    entry_type: Optional[str] = None,
    fixtures_dir: Optional[Path] = None,
) -> list[LoreEntry]:
    """Load all entries from the content directory, optionally filtered by type.

    Args:
        entry_type: Optional filter by type ('area', 'npc', 'group', 'object').
        fixtures_dir: Optional override for testing (uses fixtures instead of ~/.lore/content/).
    """
    from .config import CONTENT_DIR

    base_dir = fixtures_dir if fixtures_dir is not None else CONTENT_DIR

    entries = []

    type_dirs = {
        "area": "areas",
        "npc": "npcs",
        "group": "groups",
        "object": "objects",
    }

    if entry_type:
        dirs_to_load = [base_dir / type_dirs.get(entry_type, entry_type + "s")]
    else:
        dirs_to_load = [base_dir / d for d in type_dirs.values()]

    for directory in dirs_to_load:
        if directory.exists():
            entries.extend(load_entries_from_dir(directory))

    return entries


def find_entry_by_name(
    query: str,
    entry_type: Optional[str] = None,
    fixtures_dir: Optional[Path] = None,
) -> Optional[LoreEntry]:
    """Find an entry by name (exact match, then substring, then filename).

    Args:
        query: The search query.
        entry_type: Optional filter by type.
        fixtures_dir: Optional override for testing.
    """
    entries = load_all_entries(entry_type, fixtures_dir)
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
