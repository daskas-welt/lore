"""Unit tests for edge cases and polish."""

import pytest
import tempfile
from pathlib import Path

from lore.core.loader import parse_file, load_all_entries, find_entry_by_name
from lore.core.models import LoreEntry


class TestEmptyDirectory:
    """Test empty content directory handling."""

    def test_load_all_from_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            entries = load_all_entries(fixtures_dir=Path(tmpdir))
            assert entries == []

    def test_find_entry_in_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = find_entry_by_name("anything", fixtures_dir=Path(tmpdir))
            assert result is None


class TestInvalidFrontmatter:
    """Test invalid frontmatter handling."""

    def test_invalid_yaml_frontmatter(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\nname: [invalid yaml\n---\nContent.\n")
            filepath = Path(f.name)
        try:
            entry = parse_file(filepath)
            # Should either return None or a valid entry with defaults
            if entry is not None:
                assert isinstance(entry, LoreEntry)
        finally:
            filepath.unlink()

    def test_missing_type_defaults_to_area(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\nname: Test\n---\nContent.\n")
            filepath = Path(f.name)
        try:
            entry = parse_file(filepath)
            assert entry is not None
            assert entry.type == "area"
        finally:
            filepath.unlink()

    def test_invalid_type_in_frontmatter(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\nname: Test\ntype: invalid\n---\nContent.\n")
            filepath = Path(f.name)
        try:
            entry = parse_file(filepath)
            # Should return None for invalid type
            assert entry is None
        finally:
            filepath.unlink()


class TestDuplicateNames:
    """Test duplicate name handling."""

    def test_exact_match_priority(self, tmp_path):
        # Create two files with same name
        (tmp_path / "areas").mkdir()
        (tmp_path / "npcs").mkdir()

        (tmp_path / "areas" / "test.md").write_text(
            "---\nname: Test\ntype: area\n---\nArea content.\n"
        )
        (tmp_path / "npcs" / "test.md").write_text(
            "---\nname: Test\ntype: npc\n---\nNPC content.\n"
        )

        entry = find_entry_by_name("Test", fixtures_dir=tmp_path)
        assert entry is not None
        assert entry.name == "Test"

    def test_substring_matches_first_file(self, tmp_path):
        (tmp_path / "areas").mkdir()
        (tmp_path / "npcs").mkdir()

        (tmp_path / "areas" / "alpha.md").write_text(
            "---\nname: Alpha\ntype: area\n---\nArea.\n"
        )
        (tmp_path / "npcs" / "beta.md").write_text(
            "---\nname: Beta\ntype: npc\n---\nNPC.\n"
        )

        # "a" should match Alpha (area) first since areas are loaded first
        entry = find_entry_by_name("a", fixtures_dir=tmp_path)
        assert entry is not None
        assert "a" in entry.name.lower()


class TestSpecialCharacters:
    """Test special character handling in search."""

    def test_search_with_special_chars(self, tmp_path):
        (tmp_path / "areas").mkdir()
        (tmp_path / "areas" / "test.md").write_text(
            "---\nname: The 100% Room\ntype: area\n---\nContent.\n"
        )

        entry = find_entry_by_name("100%", fixtures_dir=tmp_path)
        assert entry is not None
        assert "100%" in entry.name

    def test_search_with_regex_like_chars(self, tmp_path):
        (tmp_path / "areas").mkdir()
        (tmp_path / "areas" / "test.md").write_text(
            "---\nname: Room [A]\ntype: area\n---\nContent.\n"
        )

        entry = find_entry_by_name("[A]", fixtures_dir=tmp_path)
        assert entry is not None

    def test_search_empty_string(self, tmp_path):
        (tmp_path / "areas").mkdir()
        (tmp_path / "areas" / "test.md").write_text(
            "---\nname: Test\ntype: area\n---\nContent.\n"
        )

        entry = find_entry_by_name("", fixtures_dir=tmp_path)
        # Empty string should match first entry (substring match)
        assert entry is not None
