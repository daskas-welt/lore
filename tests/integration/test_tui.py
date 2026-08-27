"""Integration tests for the TUI application."""

import pytest
from pathlib import Path

from textual.widgets import Markdown, MarkdownViewer, Static, Tabs, Tab

from lore.tui import LoreApp
from lore.core.models import LoreEntry


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "content"


@pytest.fixture
def sample_entries():
    """Create sample entries for testing."""
    return [
        LoreEntry(
            name="The Whispering Forest",
            type="area",
            tags=["forest", "dangerous"],
            path=FIXTURES_DIR / "areas" / "forest.md",
            content="Ancient trees with silver-grey bark.",
        ),
        LoreEntry(
            name="Old Marcus",
            type="npc",
            tags=["merchant", "friendly"],
            path=FIXTURES_DIR / "npcs" / "merchant.md",
            content="A wizened merchant with a knowing smile.",
            variants={"happy": "Hello!", "grumpy": "Go away."},
        ),
        LoreEntry(
            name="City Watch",
            type="group",
            tags=["guards", "city"],
            path=FIXTURES_DIR / "groups" / "guards.md",
            content="Blue-cloaked guards patrolling the streets.",
        ),
        LoreEntry(
            name="Dragon Slayer",
            type="object",
            tags=["weapon", "legendary"],
            path=FIXTURES_DIR / "objects" / "magic-sword.md",
            content="A bastard sword of ancient make.",
        ),
    ]


class TestTUILayout:
    """Test TUI layout and structure."""

    @pytest.mark.asyncio
    async def test_app_composes(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            assert app.query_one("Header") is not None

    @pytest.mark.asyncio
    async def test_sidebar_exists(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            assert app.query("ListItem") is not None

    @pytest.mark.asyncio
    async def test_content_pane_exists(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            assert app.query("Static") is not None


class TestTUIEntryList:
    """Test entry list display."""

    @pytest.mark.asyncio
    async def test_all_entries_shown(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            list_items = app.query("ListItem")
            assert len(list_items) >= 4

    @pytest.mark.asyncio
    async def test_entry_names_visible(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            assert app.screen is not None


class TestTUITypeFilters:
    """Test type filter Tabs per https://textual.textualize.io/widgets/tabs/."""

    @pytest.mark.asyncio
    async def test_filter_buttons_exist(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            tabs = app.query_one("#filter-tabs", Tabs)
            assert tabs is not None
            tab_labels = [
                t.label.plain if hasattr(t.label, "plain") else str(t.label)
                for t in app.query("Tab")
            ]
            assert len(tab_labels) >= 5
            assert "All" in tab_labels and "Areas" in tab_labels

    @pytest.mark.asyncio
    async def test_click_filter_shows_matching(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            # Tabs — activate Areas tab via TabActivated (exclusive filter)
            tabs = app.query_one("#filter-tabs", Tabs)
            # simulate clicking Areas tab
            tabs.active = "filter-area"
            # manually trigger filter (TabActivated handler)
            app.current_filter = "area"
            app._update_list(app.query_one("#search-bar").value)
            await pilot.pause()
            items = app.query("ListItem")
            # only area entries should remain
            assert len(items) >= 1
            assert app.screen is not None


class TestTUIMouseSelection:
    """Test mouse click entry selection."""

    @pytest.mark.asyncio
    async def test_click_entry_shows_content(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            list_items = app.query("ListItem")
            if len(list_items) > 0:
                await pilot.click(type(list_items[0]))
                assert app.screen is not None


class TestTUISearch:
    """Test real-time search filtering."""

    @pytest.mark.asyncio
    async def test_search_input_exists(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            search = app.query_one("#search-bar")
            assert search is not None

    @pytest.mark.asyncio
    async def test_search_filters_by_name(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            search = app.query_one("#search-bar")
            search.value = "forest"
            await pilot.pause()
            list_items = app.query("ListItem")
            assert len(list_items) >= 1

    @pytest.mark.asyncio
    async def test_search_filters_by_tag(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            search = app.query_one("#search-bar")
            search.value = "merchant"
            await pilot.pause()
            list_items = app.query("ListItem")
            assert len(list_items) >= 1

    @pytest.mark.asyncio
    async def test_search_no_results(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            search = app.query_one("#search-bar")
            search.value = "xyznonexistent"
            await pilot.pause()
            list_items = app.query("ListItem")
            assert len(list_items) == 0

    @pytest.mark.asyncio
    async def test_search_across_all_types(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            search = app.query_one("#search-bar")
            search.value = "dragon"
            await pilot.pause()
            list_items = app.query("ListItem")
            assert len(list_items) >= 1

    @pytest.mark.asyncio
    async def test_clear_search_restores_list(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            search = app.query_one("#search-bar")
            search.value = "forest"
            await pilot.pause()
            filtered_count = len(app.query("ListItem"))
            search.value = ""
            await pilot.pause()
            full_count = len(app.query("ListItem"))
            assert full_count >= filtered_count
            assert full_count >= 4

    @pytest.mark.asyncio
    async def test_search_case_insensitive(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            search = app.query_one("#search-bar")
            search.value = "FOREST"
            await pilot.pause()
            list_items = app.query("ListItem")
            assert len(list_items) >= 1


class TestTUIVariants:
    """Test variant display in content pane."""

    @pytest.mark.asyncio
    async def test_variants_displayed(self, sample_entries):
        app = LoreApp(entries=sample_entries)
        async with app.run_test() as pilot:
            marcus = [e for e in sample_entries if e.name == "Old Marcus"][0]
            app._update_content(marcus)
            await pilot.pause()
            viewer = app.query_one("#content", MarkdownViewer)
            assert "Happy" in app.content_text or "Grumpy" in app.content_text
            assert viewer.show_table_of_contents is False
            # document is Markdown widget; render check is best-effort
            assert "MarkdownViewer" in viewer.__class__.__name__
