"""Textual TUI — textual defaults (Button/MarkdownViewer/Footer palette)."""

from typing import Optional

from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Header,
    Footer,
    Label,
    Button,
    ListItem,
    ListView,
    Input,
    Markdown,
    MarkdownViewer,
    Tabs,
    Tab,
)
from textual import on
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.suggester import SuggestFromList

from lore.core.models import LoreEntry
from lore.core.loader import load_all_entries
from lore.core.config import get_theme, set_theme

TYPE_ICONS = {
    "area": "[*]",
    "npc": "[@]",
    "group": "[&]",
    "object": "[#]",
}


class EntryListItem(ListItem):
    """Single-line ListView row for an entry."""

    def __init__(self, entry: LoreEntry) -> None:
        self.entry = entry
        super().__init__()

    def compose(self) -> ComposeResult:
        icon = TYPE_ICONS.get(self.entry.type, "[*]")
        yield Label(f"{icon} {self.entry.name}", classes="entry-name")


class HelpScreen(ModalScreen):
    """Textual ModalScreen — textual defaults. Lifecycle: compose → on_mount."""

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
        background: $background 60%;
    }
    #help-dialog {
        width: 72;
        height: auto;
        max-height: 26;
        border: solid $primary;
        background: $panel;
        padding: 1 2;
    }
    #help-title { text-style: bold; padding: 0 0 1 0; }
    #help-body { height: auto; max-height: 16; }
    #help-close { margin-top: 1; width: 100%; }
    """

    BINDINGS = [
        Binding("escape", "close_help", "Close"),
        Binding("q", "close_help", "Close"),
        Binding("h", "close_help", "Close"),
        Binding("?", "close_help", "Close"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="help-dialog"):
            yield Label("Lore — Help", id="help-title")
            with VerticalScroll(id="help-body"):
                yield Markdown(
                    """**Navigation**
- `↑` / `↓` or click — select entry
- `All` / `Areas` / `NPCs` / `Groups` / `Objects` — filter by type (Tabs)
- `/` — focus search · type to filter by name/tag · `Esc` to clear
- `Enter` / click — show read-aloud MarkdownViewer at right

**Appearance**
- `t` — toggle theme via Footer (persisted `~/.lore/config.json`)

**General**
- `q` / `Ctrl+C` — close TUI (Footer Quit)
- `h` / `?` / `F1` — toggle this help
- `Ctrl+P` — command palette
- `Esc` — close help / clear search
""",
                )
            yield Button("Close (Esc / q)", id="help-close", variant="primary")

    def on_mount(self) -> None:
        # Use textual's theme (textual defaults)
        pass

    @on(Button.Pressed, "#help-close")
    def close_help(self) -> None:
        self.dismiss()

    def action_close_help(self) -> None:
        self.dismiss()


class LoreApp(App):
    """Lore TUI — Textual defaults (Footer + HelpScreen + Palette + Button + MarkdownViewer)."""

    SCREENS = {"help": HelpScreen}

    theme_mode = reactive("light")

    # Textual defaults — Tabs + ListView + Input — balanced paddings (all 1) — no Rule, no css borders
    CSS = """
    #sidebar { width: 1fr; min-width: 44; height: 100%; }
    #sidebar-header { height: 5; padding: 0 1; align: center middle; }
    #sidebar-title { width: 1fr; height: 100%; padding: 1 0 1 2; content-align: left middle; text-style: bold; }
    #filter-tabs { height: 3; width: 1fr; }
    #filter-tabs Tab { width: 1fr; height: 3; content-align: center middle; }
    #main { height: 1fr; width: 1fr; }
    #search-bar { height: 3; margin: 1 1; }
    #entry-list { height: 1fr; padding: 0; }
    #entry-list EntryListItem { height: 3; padding: 0 1; margin: 0; align: left middle; }
    #entry-list EntryListItem Label { width: 1fr; height: 1; content-align: left middle; }
    #content-pane { width: 2fr; height: 100%; }
    #content-header { width: 1fr; height: 3; padding: 1 1; text-style: bold; display: none; }
    #content { width: 1fr; height: 1fr; padding: 1 2; }
    """

    # Footer — left: Quit/Search/Help, right: Palette (^p) via ENABLE_COMMAND_PALETTE
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+c", "quit", "Quit", show=False),
        Binding("t", "toggle_theme", "Theme", show=False),
        Binding("/", "focus_search", "Search"),
        Binding("h", "help", "Help"),
        Binding("?", "help", "Help"),
        Binding("f1", "help", "Help", show=False),
        Binding("ctrl+p", "command_palette", "Palette", show=False),
        Binding("ctrl+k", "command_palette", "Palette", show=False),
    ]

    ENABLE_COMMAND_PALETTE = True

    def __init__(self, entries: Optional[list[LoreEntry]] = None, **kwargs):
        super().__init__(**kwargs)
        self.all_entries = entries or []
        self.current_filter: Optional[str] = None
        self.selected_entry: Optional[LoreEntry] = None
        self.content_text: str = ""
        # end-user persisted theme (light default, codegraph)
        try:
            self.theme_mode = get_theme()
        except Exception:
            self.theme_mode = "light"
        self.title = "Lore"
        self.sub_title = "read-aloud"

    def get_system_commands(self, screen):
        """Palette — Footer Palette → Ctrl+P; exposes Quit/Help/Theme for keyboard palette."""
        for cmd in super().get_system_commands(screen):
            yield cmd
        yield SystemCommand("Quit Lore", "Quit the app (q)", lambda: self.exit())
        yield SystemCommand(
            "Show Help", "Show help screen (h/?)", lambda: self.push_screen("help")
        )
        yield SystemCommand(
            "Toggle Theme", "Toggle light/dark (t)", self.action_toggle_theme
        )
        yield SystemCommand(
            "Focus Search", "Focus search bar (/)", self.action_focus_search
        )

    def _update_suggester(self) -> None:
        # Input suggester per https://textual.textualize.io/widgets/input/#suggestions — SuggestFromList for name/tag autocomplete
        try:
            suggestions: list[str] = []
            for e in self.all_entries:
                suggestions.append(e.name)
                suggestions.extend(e.tags)
            # deduplicate preserve order, case-insensitive autocomplete
            seen: set[str] = set()
            uniq: list[str] = []
            for s in suggestions:
                low = s.lower()
                if low not in seen:
                    seen.add(low)
                    uniq.append(s)
            inp = self.query_one("#search-bar", Input)
            inp.suggester = SuggestFromList(uniq, case_sensitive=False)
        except Exception:
            pass

    def on_mount(self) -> None:
        self._apply_theme(self.theme_mode)
        if not self.all_entries:
            self.all_entries = load_all_entries()
        if not self.all_entries:
            viewer = self.query_one("#content", MarkdownViewer)
            viewer.document.update(
                "## No content found\n\n"
                "Add entries to `~/.lore/content/` — subfolders:\n"
                "- `areas/`  `npcs/`  `groups/`  `objects/`\n\n"
                "Formats: `.md` (YAML frontmatter), `.yaml`, `.json`\n\n"
                "Press `q` to quit · `h` for help · `Ctrl+P` palette"
            )
        self._update_suggester()
        self._update_list()

    def _apply_theme(self, mode: str) -> None:
        # Textual defaults: use built-in theme + dark flag (Footer Theme)
        self.theme = "textual-dark" if mode == "dark" else "textual-light"
        self.dark = mode == "dark"

    def action_toggle_theme(self) -> None:
        self.theme_mode = "dark" if self.theme_mode == "light" else "light"
        set_theme(self.theme_mode)
        self._apply_theme(self.theme_mode)

    def action_help(self) -> None:
        try:
            self.push_screen("help")
        except Exception:
            self.push_screen(HelpScreen())

    def action_focus_search(self) -> None:
        self.query_one("#search-bar", Input).focus()

    def on_key(self, event) -> None:
        if event.key == "escape":
            search = self.query_one("#search-bar", Input)
            if search.value:
                search.value = ""
                self._update_list()
                event.stop()

    # ── List helpers ──────────────────────────────────────────────────
    def compose(self) -> ComposeResult:
        yield Header()
        # Tabs below Header — full width, then left/right areas (ListView left, MarkdownViewer right)
        yield Tabs(
            Tab("All", id="filter-all"),
            Tab("Areas", id="filter-area"),
            Tab("NPCs", id="filter-npc"),
            Tab("Groups", id="filter-group"),
            Tab("Objects", id="filter-object"),
            id="filter-tabs",
        )
        with Horizontal(id="main"):
            with Vertical(id="sidebar"):
                # Search — Input with SuggestFromList per https://textual.textualize.io/widgets/input/
                yield Input(placeholder="Search entries…", id="search-bar")
                # Left panel — Textual ListView per https://textual.textualize.io/widgets/list_view/
                # Displays vertical ListItem(Label) list; BINDINGS enter/up/down, Messages Highlighted/Selected
                yield ListView(id="entry-list")
            with Vertical(id="content-pane"):
                yield Label("", id="content-header")
                yield MarkdownViewer(
                    "",
                    show_table_of_contents=False,
                    id="content",
                )
        yield Footer()

    def _get_filtered_entries(self) -> list[LoreEntry]:
        if self.current_filter is None:
            return self.all_entries
        return [e for e in self.all_entries if e.type == self.current_filter]

    def _update_list(self, search_query: str = "") -> None:
        # ListView per https://textual.textualize.io/widgets/list_view/ — clear/append/index/Highlighted/Selected
        entries = self._get_filtered_entries()
        if search_query:
            q = search_query.lower()
            entries = [
                e
                for e in entries
                if q in e.name.lower() or any(q in t.lower() for t in e.tags)
            ]
        lv = self.query_one("#entry-list", ListView)
        lv.clear()  # ListView.clear() — docs: clear all items
        for entry in entries:
            # ListView rows use the documented ListItem container with Label children.
            item = EntryListItem(entry)
            lv.append(item)  # ListView.append(item) — docs: append ListItem
        # Ensure ListView highlight resets so entries are visible after Tabs filter
        try:
            lv.index = 0 if entries else None
        except Exception:
            pass

    def _update_content(self, entry: LoreEntry) -> None:
        self.selected_entry = entry
        header = self.query_one("#content-header", Label)
        viewer = self.query_one("#content", MarkdownViewer)
        header.display = True
        header.styles.display = "block"
        icon = TYPE_ICONS.get(entry.type, "")
        header.update(f"  {icon}  {entry.name}")
        # MarkdownViewer: use document.update (Markdown widget inside viewer)
        body = entry.content.strip()
        parts: list[str] = []
        if entry.tags:
            # Textual defaults: inline code badges `#tag` (MarkdownViewer renders)
            tags = " ".join(f"`#{t}`" for t in entry.tags)
            parts.append(tags)
            parts.append("")
        parts.append(body)
        if entry.variants:
            parts.append("")
            parts.append("---")
            parts.append("")
            parts.append("### Variants")
            parts.append("")
            for key, value in entry.variants.items():
                # value may itself be markdown
                parts.append(f"**{key.title()}:** {value}")
                parts.append("")
        self.content_text = "\n".join(parts).strip()
        viewer.document.update(self.content_text)
        # keep TOC off even if content triggers it
        viewer.show_table_of_contents = False

    @on(Tabs.TabActivated, "#filter-tabs")
    def on_filter_tab(self, event: Tabs.TabActivated) -> None:
        # Tabs per https://textual.textualize.io/widgets/tabs/ — TabActivated message carries tab.id
        tab_id = event.tab.id if event.tab and event.tab.id else ""
        mapping: dict[str, Optional[str]] = {
            "filter-all": None,
            "filter-area": "area",
            "filter-npc": "npc",
            "filter-group": "group",
            "filter-object": "object",
        }
        self.current_filter = mapping.get(tab_id)
        self._update_list(self.query_one("#search-bar", Input).value)

    @on(Input.Changed, "#search-bar")
    def on_search_changed(self, event: Input.Changed) -> None:
        self._update_list(search_query=event.value)

    @on(Input.Submitted, "#search-bar")
    def on_search_submitted(self, event: Input.Submitted) -> None:
        # Enter selects first filtered entry
        lv = self.query_one("#entry-list", ListView)
        if lv.children:
            lv.index = 0
            # trigger Selected via enter not needed; focus stays
            pass

    @on(ListView.Selected)
    def on_entry_selected(self, event: ListView.Selected) -> None:
        if event.item is not None and hasattr(event.item, "entry"):
            self._update_content(event.item.entry)  # type: ignore[attr-defined]


def main():
    app = LoreApp()
    app.run()


if __name__ == "__main__":
    main()
