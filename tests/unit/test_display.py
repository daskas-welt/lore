"""Unit tests for the display module."""

import pytest
from io import StringIO

from lore.core.models import LoreEntry
from lore.core.display import (
    render_entry,
    render_list,
    render_error,
    render_success,
    render_info,
)
from rich.console import Console


@pytest.fixture
def mock_console(monkeypatch):
    """Create a console that captures output."""
    output = StringIO()
    console = Console(file=output, force_terminal=True, width=80)
    monkeypatch.setattr("lore.core.display.console", console)
    return console, output


class TestRenderEntry:
    """Test rendering a single entry."""

    def test_render_entry_shows_name(self, mock_console):
        _, output = mock_console
        entry = LoreEntry(
            name="Forest",
            type="area",
            tags=["dark"],
            path="forest.md",
            content="A dark forest.",
        )
        render_entry(entry)
        assert "Forest" in output.getvalue()

    def test_render_entry_shows_type(self, mock_console):
        _, output = mock_console
        entry = LoreEntry(
            name="Marcus",
            type="npc",
            tags=[],
            path="marcus.md",
            content="A merchant.",
        )
        render_entry(entry)
        assert "NPC" in output.getvalue()

    def test_render_entry_shows_tags(self, mock_console):
        _, output = mock_console
        entry = LoreEntry(
            name="Sword",
            type="object",
            tags=["weapon", "magical"],
            path="sword.md",
            content="A sword.",
        )
        render_entry(entry)
        assert "weapon" in output.getvalue()
        assert "magical" in output.getvalue()

    def test_render_entry_shows_content(self, mock_console):
        _, output = mock_console
        entry = LoreEntry(
            name="Forest",
            type="area",
            tags=[],
            path="forest.md",
            content="The ancient trees tower above you.",
        )
        render_entry(entry)
        assert "ancient trees" in output.getvalue()

    def test_render_entry_shows_variants(self, mock_console):
        _, output = mock_console
        entry = LoreEntry(
            name="Marcus",
            type="npc",
            tags=[],
            path="marcus.md",
            content="A merchant.",
            variants={"happy": "Hello!", "grumpy": "Go away."},
        )
        render_entry(entry)
        assert "Happy" in output.getvalue()
        assert "Grumpy" in output.getvalue()

    def test_render_entry_no_variants_section_when_empty(self, mock_console):
        _, output = mock_console
        entry = LoreEntry(
            name="Forest",
            type="area",
            tags=[],
            path="forest.md",
            content="A forest.",
        )
        render_entry(entry)
        assert "variant" not in output.getvalue().lower()

    def test_render_entry_empty_content(self, mock_console):
        _, output = mock_console
        entry = LoreEntry(
            name="Empty",
            type="area",
            tags=[],
            path="empty.md",
            content="",
        )
        render_entry(entry)
        assert "Empty" in output.getvalue()


class TestRenderList:
    """Test rendering a list of entries."""

    def test_render_list_shows_title(self, mock_console):
        _, output = mock_console
        items = [{"name": "Forest", "tags": ["dark"]}]
        render_list("Areas", items, ["Name", "Tags"])
        assert "Areas" in output.getvalue()

    def test_render_list_shows_items(self, mock_console):
        _, output = mock_console
        items = [
            {"name": "Forest", "tags": ["dark"]},
            {"name": "Swamp", "tags": ["wet"]},
        ]
        render_list("Locations", items, ["Name", "Tags"])
        assert "Forest" in output.getvalue()
        assert "Swamp" in output.getvalue()

    def test_render_list_empty(self, mock_console):
        _, output = mock_console
        render_list("Empty", [], ["Name"])
        assert "Empty" in output.getvalue()

    def test_render_list_multiple_columns(self, mock_console):
        _, output = mock_console
        items = [{"name": "Marcus", "role": "merchant", "tags": ["friendly"]}]
        render_list("NPCs", items, ["Name", "Role", "Tags"])
        assert "Marcus" in output.getvalue()
        assert "merchant" in output.getvalue()
        assert "friendly" in output.getvalue()


class TestRenderMessages:
    """Test error, success, and info messages."""

    def test_render_error(self, mock_console):
        _, output = mock_console
        render_error("Something went wrong")
        assert "Something went wrong" in output.getvalue()

    def test_render_success(self, mock_console):
        _, output = mock_console
        render_success("File saved")
        assert "File saved" in output.getvalue()

    def test_render_info(self, mock_console):
        _, output = mock_console
        render_info("FYI: something")
        assert "FYI" in output.getvalue()
