"""Unit tests for the loader module."""

import pytest
import tempfile
import yaml
from pathlib import Path

from lore.core.loader import (
    parse_file,
    load_entries_from_dir,
    load_all_entries,
    find_entry_by_name,
)


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "content"


class TestParseMarkdown:
    """Test Markdown file parsing."""

    def test_parse_valid_markdown(self):
        filepath = FIXTURES_DIR / "areas" / "forest.md"
        entry = parse_file(filepath)

        assert entry is not None
        assert entry.name == "The Whispering Forest"
        assert entry.type == "area"
        assert "forest" in entry.tags
        assert "dangerous" in entry.tags
        assert "magical" in entry.tags
        assert "ancient" in entry.content.lower()

    def test_parse_markdown_with_variants(self):
        filepath = FIXTURES_DIR / "npcs" / "merchant.md"
        entry = parse_file(filepath)

        assert entry is not None
        assert entry.name == "Old Marcus"
        assert "happy" in entry.variants
        assert "grumpy" in entry.variants

    def test_parse_markdown_without_frontmatter(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Just a heading\n\nSome content.\n")
            filepath = Path(f.name)

        try:
            entry = parse_file(filepath)
            assert entry is not None
            assert entry.name == "Just a heading"
            assert entry.type == "area"  # default
        finally:
            filepath.unlink()

    def test_parse_nonexistent_file(self):
        entry = parse_file(Path("/nonexistent/file.md"))
        assert entry is None


class TestParseYaml:
    """Test YAML file parsing."""

    def test_parse_valid_yaml(self):
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
            assert "test" in entry.tags
            assert entry.content == "A test NPC."
        finally:
            filepath.unlink()

    def test_parse_yaml_with_variants(self):
        yaml_content = {
            "name": "NPC",
            "type": "npc",
            "description": "An NPC.",
            "variants": {"happy": "Hi!", "sad": "Bye."},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            yaml.dump(yaml_content, f)
            filepath = Path(f.name)

        try:
            entry = parse_file(filepath)
            assert entry is not None
            assert entry.variants == {"happy": "Hi!", "sad": "Bye."}
        finally:
            filepath.unlink()


class TestParseJson:
    """Test JSON file parsing."""

    def test_parse_valid_json(self):
        import json

        json_content = {
            "name": "Test Object",
            "type": "object",
            "tags": ["test"],
            "description": "A test object.",
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(json_content, f)
            filepath = Path(f.name)

        try:
            entry = parse_file(filepath)
            assert entry is not None
            assert entry.name == "Test Object"
            assert entry.type == "object"
            assert entry.content == "A test object."
        finally:
            filepath.unlink()


class TestLoadEntriesFromDir:
    """Test loading entries from a directory."""

    def test_load_from_areas(self):
        entries = load_entries_from_dir(FIXTURES_DIR / "areas")
        assert len(entries) == 1
        assert entries[0].name == "The Whispering Forest"

    def test_load_from_npcs(self):
        entries = load_entries_from_dir(FIXTURES_DIR / "npcs")
        assert len(entries) == 1
        assert entries[0].name == "Old Marcus"

    def test_load_from_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            entries = load_entries_from_dir(Path(tmpdir))
            assert entries == []

    def test_load_from_nonexistent_dir(self):
        entries = load_entries_from_dir(Path("/nonexistent/dir"))
        assert entries == []


class TestLoadAllEntries:
    """Test loading all entries from content directory."""

    def test_load_all_from_fixtures(self):
        entries = load_all_entries(fixtures_dir=FIXTURES_DIR)
        names = [e.name for e in entries]
        assert "The Whispering Forest" in names
        assert "Old Marcus" in names
        assert "City Watch" in names
        assert "Dragon Slayer" in names

    def test_load_all_by_type(self):
        areas = load_all_entries(entry_type="area", fixtures_dir=FIXTURES_DIR)
        assert len(areas) == 1
        assert areas[0].type == "area"

    def test_load_all_npcs(self):
        npcs = load_all_entries(entry_type="npc", fixtures_dir=FIXTURES_DIR)
        assert len(npcs) == 1
        assert npcs[0].type == "npc"


class TestFindEntryByName:
    """Test finding entries by name."""

    def test_exact_match(self):
        entry = find_entry_by_name("The Whispering Forest", fixtures_dir=FIXTURES_DIR)
        assert entry is not None
        assert entry.name == "The Whispering Forest"

    def test_case_insensitive_exact(self):
        entry = find_entry_by_name("the whispering forest", fixtures_dir=FIXTURES_DIR)
        assert entry is not None
        assert entry.name == "The Whispering Forest"

    def test_substring_match(self):
        entry = find_entry_by_name("whisper", fixtures_dir=FIXTURES_DIR)
        assert entry is not None
        assert "Whisper" in entry.name

    def test_no_match(self):
        entry = find_entry_by_name("nonexistent", fixtures_dir=FIXTURES_DIR)
        assert entry is None

    def test_filter_by_type(self):
        entry = find_entry_by_name(
            "Marcus", entry_type="npc", fixtures_dir=FIXTURES_DIR
        )
        assert entry is not None
        assert entry.type == "npc"

    def test_filter_by_type_no_match(self):
        entry = find_entry_by_name(
            "Marcus", entry_type="area", fixtures_dir=FIXTURES_DIR
        )
        assert entry is None
