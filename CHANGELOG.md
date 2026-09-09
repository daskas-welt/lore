# Changelog

All notable changes to Lore will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-09-09

### Fixed
- Bundle `rich` (and `rich.panel`/`rich.text`) in PyInstaller exe and install project deps in Release workflow — `v0.2.0` exe crashed with `ModuleNotFoundError: No module named 'rich'` (lore.spec, .github/workflows/release.yml)
- Bundle all `textual` lazy-loaded widgets (`_markdown_viewer`, `_tabs`, `_list_view`, etc.) — `v0.2.1` pre-release crashed with `No module named 'textual.widgets._markdown_viewer'` (lore.spec)
- Build exe as console app (`console=True` in lore.spec) — windowed build left `stdin` as `None`, crashing Textual's Win32 driver on `fileno()` when double-clicked

## [0.2.0] - 2026-09-09

### Added
- Emoji type icons in entry list and content header: ⛰️ area, 🧙 npc, ⚔️ group, 🗡️ object (src/lore/tui.py:30)
- Polished typography for right pane: gold italic **📖 Read-Aloud** callout plus DM-reference strip (Atmosphere / Hazards / Hooks / Sounds) parsed from inline `Key:` sections in entry content (src/lore/tui.py:split_sections)

### Fixed
- Move `dependencies` out of `[project.urls]` in pyproject.toml — built wheels previously declared zero runtime dependencies so `pip install lore` succeeded without `textual`/`rich` etc. (pyproject.toml)

## [0.1.0] - 2026-08-27

### Added
- Full-screen TUI built with Textual
- Tab navigation: All, Areas, NPCs, Groups, Objects
- Live search with `SuggestFromList` autocomplete
- Markdown rendering of entry content
- Command palette (`ctrl+backslash`)
- Light/dark theme toggle persisted to `~/.lore/config.json`
- `load_all_entries(entry_type=None)` with optional `fixtures_dir` parameter
- Content loader with YAML/JSON/Markdown frontmatter parsing
- 79 generic, reusable entries across all four types
- Integration tests for TUI workflow
- PyInstaller builds for Windows and Linux via `lore.spec`

[0.1.0]: https://github.com/daskas-welt/lore/releases/tag/v0.1.0
