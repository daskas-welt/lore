# Implementation Plan: Read-Aloud Display

**Branch**: `002-read-aloud-display` | **Date**: 2026-08-27 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-read-aloud-display/spec.md`

## Summary

Rewrite Lore from scratch as a TUI-only read-aloud display tool for dungeon masters. The DM browses content (areas, NPCs, groups, objects) via an interactive Textual TUI. All text is read-aloud ready — formatted for natural reading during tabletop sessions. The TUI supports mouse-driven navigation, clickable type filters, and real-time search across all entry types. Implementation follows TDD with tests written alongside each component.

## Technical Context

**Language/Version**: Python 3.10+

**Primary Dependencies**:
- `rich` — Terminal formatting and rendering
- `textual` — TUI framework
- `python-frontmatter` — Markdown frontmatter parsing
- `pyyaml` — YAML file parsing
- `markdown` — Markdown rendering

**Dev Dependencies**:
- `pytest` + `pytest-cov` — Testing
- `textual-dev` — TUI dev tools (live reload, debugger)
- `pyinstaller` — Build standalone executables

**Storage**: Local files in `~/.lore/content/{areas,npcs,groups,objects}/`

**Testing**: `pytest` with `pytest-cov`

**Target Platform**: Cross-platform terminal (Windows, macOS, Linux)

**Project Type**: TUI desktop application

**Performance Goals**: Entry selection < 1s, search filter < 500ms

**Constraints**: Offline-only, single-user, no network dependencies

**Scale/Scope**: Up to 1000 entries, 4 content types

## Constitution Check

*Lore Constitution principles:*
1. **Speed** — Fast retrieval at the table. No friction.
2. **Simplicity** — Flat content structure. No campaigns, no nested hierarchies.
3. **Read-aloud ready** — Content formatted for immersive reading, not editing.
4. **Offline-first** — All data is local files. No network required.

All principles satisfied. No violations.

## Project Structure

### Documentation (this feature)

```text
specs/002-read-aloud-display/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Task list (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/lore/
├── __init__.py              # Package version
├── tui.py                   # Textual TUI application
├── core/
│   ├── __init__.py
│   ├── config.py            # Path management (~/.lore/)
│   ├── models.py            # LoreEntry dataclass
│   ├── loader.py            # File parsing (MD/YAML/JSON) + entry loading
│   └── display.py           # Rich-based rendering for TUI content pane

tests/
├── integration/
│   └── test_tui.py          # TUI integration tests
└── unit/
    ├── test_loader.py       # File parsing tests
    ├── test_models.py       # Model validation tests
    └── test_display.py      # Display rendering tests

.github/
└── workflows/
    └── release.yml          # Build + release on tag push

lore.spec                    # PyInstaller spec (shared)
```

**Structure Decision**: Single project layout. TUI is the only interface. Core modules (config, models, loader, display) are shared and independently testable.

## Implementation Phases

### Phase 1: Core Foundation (TDD)

Build the data layer and file parsing — the foundation everything else depends on.

| Step | What | Tests First |
|------|------|-------------|
| 1.1 | `LoreEntry` dataclass with validation | `test_models.py` |
| 1.2 | Config paths (`~/.lore/content/`) | `test_config.py` |
| 1.3 | File parsers (Markdown, YAML, JSON) | `test_loader.py` |
| 1.4 | `load_all_entries()` and `find_entry_by_name()` | `test_loader.py` |

**Exit criteria**: All unit tests pass. Can parse sample content files into `LoreEntry` objects.

### Phase 2: Display Layer (TDD)

Build the Rich-based rendering used by the TUI content pane.

| Step | What | Tests First |
|------|------|-------------|
| 2.1 | `render_entry()` — single entry display | `test_display.py` |
| 2.2 | `render_list()` — typed list display | `test_display.py` |

**Exit criteria**: Can render entries and lists to terminal with proper formatting.

### Phase 3: TUI — Browse and Select (TDD) 🎯 MVP

Build the Textual TUI with core interaction features.

| Step | What | Tests First |
|------|------|-------------|
| 3.1 | Basic layout (sidebar + content pane) | `test_tui.py` |
| 3.2 | Entry list with mouse click selection | `test_tui.py` |
| 3.3 | Clickable type filter buttons | `test_tui.py` |
| 3.4 | Content pane with formatted display | `test_tui.py` |

**Exit criteria**: TUI launches, shows entries, supports click selection and type filtering.

### Phase 4: Search (TDD)

Add real-time search across all entry types.

| Step | What | Tests First |
|------|------|-------------|
| 4.1 | Search input widget | `test_tui.py` |
| 4.2 | Real-time filter by name and tags | `test_tui.py` |
| 4.3 | Empty results state | `test_tui.py` |

**Exit criteria**: Search works across all types in real time.

### Phase 5: Polish & Edge Cases

| Step | What |
|------|------|
| 5.1 | Empty content directory message |
| 5.2 | Invalid frontmatter warnings |
| 5.3 | Duplicate name handling |
| 5.4 | Special character search handling |

**Exit criteria**: All edge cases from spec handled gracefully.

### Phase 6: Distribution

Build standalone executables and set up automated releases.

| Step | What |
|------|------|
| 6.1 | PyInstaller spec for Windows exe |
| 6.2 | PyInstaller spec for Linux binary |
| 6.3 | GitHub Actions workflow for automated builds |
| 6.4 | GitHub Releases setup with binary uploads |

**Exit criteria**: `pyinstaller` produces working exe (Windows) and binary (Linux). GitHub Actions builds and uploads on tag push.

## Build Order

```
Phase 1 (Core) → Phase 2 (Display) → Phase 3 (TUI) → Phase 4 (Search) → Phase 5 (Polish) → Phase 6 (Distribution)
```

Each phase is independently testable. The TUI (Phase 3) is the first user-facing deliverable. Distribution (Phase 6) happens after the TUI is complete and polished.

## Risk Areas

| Risk | Mitigation |
|------|-----------|
| Textual learning curve | Start with minimal TUI, iterate |
| Frontmatter parsing edge cases | Comprehensive test fixtures |
| Cross-platform path handling | Use `pathlib.Path` throughout |
