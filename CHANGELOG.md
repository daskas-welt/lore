# Changelog

All notable changes to Lore will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.0]: https://github.com/user/lore/releases/tag/v0.1.0
