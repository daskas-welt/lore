# Tasks: Read-Aloud Display

**Input**: Design documents from `/specs/002-read-aloud-display/`

**Prerequisites**: plan.md, spec.md

**Tests**: TDD — write tests FIRST, ensure they FAIL before implementation.

**Organization**: Tasks are grouped by user story. Each story can be implemented and tested independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1, US2)

---

## Phase 1: Core Foundation (Shared Infrastructure)

**Purpose**: Data models, config, and file parsing — everything depends on this.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

### Tests

- [x] T001 [P] Unit tests for `LoreEntry` model validation in `tests/unit/test_models.py`
- [x] T002 [P] Unit tests for config path resolution in `tests/unit/test_config.py`
- [x] T003 [P] Unit tests for Markdown/YAML/JSON file parsing in `tests/unit/test_loader.py`
- [x] T004 [P] Unit tests for `load_all_entries()` and `find_entry_by_name()` in `tests/unit/test_loader.py`

### Implementation

- [x] T005 [P] Create `LoreEntry` dataclass with type validation in `src/lore/core/models.py`
- [x] T006 [P] Create config module with `CONTENT_DIR` and `ensure_content_dir()` in `src/lore/core/config.py`
- [x] T007 Implement `_parse_markdown()`, `_parse_yaml()`, `_parse_json()` in `src/lore/core/loader.py`
- [x] T008 Implement `load_all_entries(entry_type)` and `find_entry_by_name(query, entry_type)` in `src/lore/core/loader.py`

**Checkpoint**: All unit tests pass. Can parse content files into LoreEntry objects.

---

## Phase 2: Display Layer (TUI Rendering)

**Purpose**: Rich-based rendering used by the TUI content pane.

### Tests

- [x] T009 [P] Unit tests for `render_entry()` output in `tests/unit/test_display.py`
- [x] T010 [P] Unit tests for `render_list()` output in `tests/unit/test_display.py`

### Implementation

- [x] T011 [P] Implement `render_entry()` with title, tags, content, variants in `src/lore/core/display.py`
- [x] T012 [P] Implement `render_list()` with typed table layout in `src/lore/core/display.py`
- [x] T013 [P] Implement `render_error()` and `render_success()` message helpers in `src/lore/core/display.py`

**Checkpoint**: Can render entries and lists to terminal with proper formatting.

---

## Phase 3: User Story 1 — Browse and Select Entry from List (Priority: P1) 🎯 MVP

**Goal**: DM launches TUI, sees entries in sidebar, clicks one to display, uses clickable type filters.

**Independent Test**: Launch TUI, see entry list, click an entry, read the formatted text.

### Tests

- [x] T014 [P] [US1] Integration test for TUI launch and entry list display in `tests/integration/test_tui.py`
- [x] T015 [P] [US1] Integration test for mouse click entry selection in `tests/integration/test_tui.py`
- [x] T016 [P] [US1] Integration test for clickable type filter buttons in `tests/integration/test_tui.py`
- [x] T017 [P] [US1] Integration test for content pane display after selection in `tests/integration/test_tui.py`

### Implementation

- [x] T018 [US1] Create Textual app with sidebar + content pane layout in `src/lore/tui.py`
- [x] T019 [US1] Implement entry list widget with mouse click handler in `src/lore/tui.py`
- [x] T020 [US1] Implement clickable type filter buttons (All, Areas, NPCs, Groups, Objects) in `src/lore/tui.py`
- [x] T021 [US1] Implement content pane with formatted entry display in `src/lore/tui.py`

**Checkpoint**: TUI launches, shows entries, supports click selection and type filtering.

---

## Phase 4: User Story 2 — Quick Search and Filter (Priority: P2)

**Goal**: DM types in search bar and entry list filters in real time across all types.

**Independent Test**: Type a search query, verify list filters instantly. Clear search, verify full list returns.

### Tests

- [x] T022 [P] [US2] Integration test for real-time search filtering in `tests/integration/test_tui.py`
- [x] T023 [P] [US2] Integration test for empty search results message in `tests/integration/test_tui.py`
- [x] T024 [P] [US2] Integration test for search clearing restores full list in `tests/integration/test_tui.py`

### Implementation

- [x] T025 [US2] Add search input widget to TUI sidebar in `src/lore/tui.py`
- [x] T026 [US2] Implement real-time filter across all entry types by name and tags in `src/lore/tui.py`
- [x] T027 [US2] Handle empty results state with "no matches" message in `src/lore/tui.py`

**Checkpoint**: Search works across all types in real time.

---

## Phase 5: Polish & Edge Cases

**Purpose**: Handle edge cases from spec, ensure robustness.

- [x] T028 [P] Empty content directory: show helpful message pointing to `~/.lore/content/` in `src/lore/tui.py`
- [x] T029 [P] Invalid frontmatter: skip file and warn user (not crash) in `src/lore/core/loader.py`
- [x] T030 [P] Duplicate names: exact match priority over substring in `src/lore/core/loader.py`
- [x] T031 [P] Special characters in search: treat as literal string in `src/lore/core/loader.py`
- [x] T032 Run full test suite and verify all pass

---

## Phase 6: Distribution

**Purpose**: Build standalone executables and set up automated releases.

- [x] T033 Create PyInstaller spec file for Windows exe in `lore.spec`
- [x] T034 Create PyInstaller spec file for Linux binary in `lore.spec`
- [x] T035 Create GitHub Actions workflow for build + release in `.github/workflows/release.yml`
- [ ] T036 Test build on Windows (exe) and Linux (binary)
- [ ] T037 Verify GitHub Release uploads on tag push

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Foundation)**: No dependencies — start immediately
- **Phase 2 (Display)**: Depends on Phase 1 (uses models, loader)
- **Phase 3 (TUI / US1)**: Depends on Phase 1 + Phase 2
- **Phase 4 (Search / US2)**: Depends on Phase 3 (TUI must exist)
- **Phase 5 (Polish)**: Depends on all user stories complete
- **Phase 6 (Distribution)**: Depends on Phase 5 (polish complete)

### Parallel Opportunities

- T001-T004: All foundation tests (parallel, different files)
- T005-T006: Model + config (parallel, different files)
- T009-T010: All display tests (parallel)
- T011-T013: All display implementations (parallel)
- T014-T017: All TUI integration tests (parallel)
- T022-T024: All search tests (parallel)

---

## Notes

- TDD enforced: tests written and verified FAILING before each implementation task
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
- Each user story delivers standalone value
- TUI is view-only: no editing, no raw view
