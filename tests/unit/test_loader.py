"""Unit tests for the loader module."""

import pytest
from pathlib import Path

from lore.core.loader import parse_file, load_entries_from_dir


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "campaigns" / "test-campaign"


def test_parse_markdown():
    """Test parsing markdown with frontmatter."""
    filepath = FIXTURES_DIR / "areas" / "forest.md"
    entry = parse_file(filepath)

    assert entry is not None
    assert entry.name == "The Whispering Forest"
    assert entry.type == "area"
    assert "forest" in entry.tags
    assert "dangerous" in entry.tags
    assert "magical" in entry.tags
    assert "ancient" in entry.content.lower()


def test_parse_yaml():
    """Test parsing YAML file."""
    # Create a test YAML file
    import tempfile
    import yaml

    yaml_content = {
        "name": "Test NPC",
        "type": "npc",
        "tags": ["test"],
        "description": "A test NPC.",
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(yaml_content, f)
        filepath = Path(f.name)

    try:
        entry = parse_file(filepath)
        assert entry is not None
        assert entry.name == "Test NPC"
        assert entry.type == "npc"
    finally:
        filepath.unlink()


def test_load_entries_from_dir():
    """Test loading entries from directory."""
    entries = load_entries_from_dir(FIXTURES_DIR / "areas")
    assert len(entries) == 1
    assert entries[0].name == "The Whispering Forest"
