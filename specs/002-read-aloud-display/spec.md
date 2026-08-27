# Feature Specification: Read-Aloud Display

**Feature Branch**: `002-read-aloud-display`

**Created**: 2026-08-27

**Status**: Draft

**Input**: User description: "Dungeon master may list areas, npc, object descriptions. A text should be displayed so that he can read it to his players."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse and Select Entry from List (Priority: P1)

As a dungeon master, I want to browse a list of all my content (areas, NPCs, objects) and select one to display, so that I can quickly find and read descriptions during a session.

**Why this priority**: This is the core interaction model. Without the ability to browse and select, the DM cannot use Lore at the table.

**Independent Test**: Can be fully tested by launching the TUI, seeing the list of entries, clicking one, and reading the displayed text.

**Acceptance Scenarios**:

1. **Given** the DM has content files in their content directory, **When** they launch the TUI, **Then** all entries (areas, NPCs, objects, groups) are listed in the sidebar.
2. **Given** the entry list is displayed, **When** the DM clicks an entry, **Then** the full read-aloud text is displayed in the main content pane.
3. **Given** the DM wants to filter by type, **When** they click the corresponding type button, **Then** only entries of that type are shown in the list.

---

### User Story 2 - Quick Search and Filter (Priority: P2)

As a dungeon master, I want to search for entries by name or tag, so that I can find content fast during a session without scrolling through a long list.

**Why this priority**: Speed matters at the table. Searching is a power-user feature that makes Lore practical for large content libraries.

**Independent Test**: Can be tested by typing a search query in the TUI search bar and verifying the list filters in real time across all entry types.

**Acceptance Scenarios**:

1. **Given** the DM is in the TUI, **When** they type in the search bar, **Then** the entry list filters to matching names and tags across all entry types in real time.
2. **Given** the DM types a query that matches no entries, **When** the filter completes, **Then** an empty list or "no results" message is shown.
3. **Given** the DM clears the search bar, **When** the input is emptied, **Then** the full entry list is restored.

---

### Edge Cases

- What happens when the content directory is empty? Show a helpful message pointing to where files should be placed.
- What happens when a content file has invalid frontmatter? Skip the file and show a warning, don't crash.
- What happens when two entries have the same name? Return the first match; exact match takes priority over substring.
- What happens when the DM searches for a special character? Treat it as a literal string, no regex.

## Clarifications

### Session 2026-08-27

- Q: How does the dungeon master navigate and select entries in the TUI? → A: Keyboard + mouse (click to select)
- Q: Should the TUI be read-only, or can the DM also edit entry text directly in the TUI? → A: Read-write (inline editing and saving)
- Q: When the DM searches, should it search across all entry types or only the currently filtered type? → A: Search across all types always
- Q: How should the DM trigger type filters (areas, NPCs, groups, objects)? → A: Clickable buttons only (no keyboard shortcuts)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display all entries from `~/.lore/content/{areas,npcs,groups,objects}/` directories.
- **FR-002**: System MUST support browsing entries via interactive TUI with sidebar list, clickable type filter buttons, and content pane.
- **FR-003**: System MUST provide real-time search/filter by name and tags across all entry types in the TUI.
- **FR-004**: System MUST render read-aloud text with clear visual formatting (title, tags, body).
- **FR-005**: System MUST display entry variants in separate labeled sections when present.
- **FR-006**: System MUST skip files with invalid frontmatter gracefully and warn the user.
- **FR-007**: System MUST prioritize exact name matches over substring matches when searching.
- **FR-008**: System MUST allow entry selection via mouse click in the TUI sidebar.

### Key Entities

- **LoreEntry**: A single content item with a name, type (area/npc/group/object), tags, content text, and optional variants.
- **Content Directory**: The flat file structure at `~/.lore/content/` where entry files are stored.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: DM can locate and display any entry within 5 seconds of launching the TUI.
- **SC-002**: 100% of valid content files are loaded without crashes.
- **SC-003**: Read-aloud text is visually clear enough that a DM can read it naturally without preparation.

## Assumptions

- All content is stored locally in `~/.lore/content/` with the existing directory structure (areas/, npcs/, groups/, objects/).
- Content files use Markdown with YAML frontmatter or YAML format (as defined in the existing spec).
- The DM is the only user; no multi-user or collaboration features are needed.
- Text is always read-aloud; there is no DM-only/private note separation.
- Performance is not a concern for libraries under 1000 entries.
