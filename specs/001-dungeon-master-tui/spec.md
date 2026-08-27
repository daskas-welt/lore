# LORE - Dungeon Master's Companion

## Overview

LORE is a CLI/TUI tool for Dungeon Masters to manage and quickly retrieve read-aloud descriptions, NPCs, locations, groups, and items during tabletop RPG sessions.

- **Version:** 2.0.0
- **Language:** Python 3.10+
- **TUI Framework:** Textual
- **CLI Framework:** Typer + Rich
- **Package:** `lore` (installed via `pip install -e .`)

## Architecture

```
src/lore/
├── cli.py                  # Typer CLI entry point
├── tui.py                  # Textual interactive TUI
├── __init__.py             # Package version
├── core/
│   ├── config.py           # Path management (~/.lore/)
│   ├── models.py           # LoreEntry dataclass
│   ├── loader.py           # File parsing (MD/YAML/JSON) + entry loading
│   └── display.py          # Rich-based terminal rendering
└── commands/
    ├── display.py          # Display entry command
    └── npc.py              # NPC/object commands
```

## Data Model

### LoreEntry

```python
@dataclass
class LoreEntry:
    name: str
    type: str           # 'area' | 'npc' | 'group' | 'object'
    tags: list[str]
    path: Path
    content: str
    frontmatter: dict
    variants: dict[str, str]   # key -> markdown content
```

### Entry Types

| Type   | Icon | Color         | List Header     |
|--------|------|---------------|-----------------|
| area   | `[*]`| bright_green  | CONTENT - LOCATIONS |
| npc    | `[@]`| bright_cyan   | TAVERN ROSTER   |
| group  | `[&]`| bright_yellow | INVENTORY       |
| object | `[#]`| bright_magenta| INVENTORY       |

### File Formats

- **Markdown** (`.md`): YAML frontmatter + body content
- **YAML** (`.yaml`/`.yml`): Full document as dict
- **JSON** (`.json`): Full document as dict

### Frontmatter Schema (Markdown)

```yaml
---
name: "Entry Name"
type: area|npc|group|object
tags: [tag1, tag2]
variants:
  variant_name: "Variant content in markdown"
---
```

## Content Storage

- **Global content:** `~/.lore/content/{areas,npcs,groups,objects}/`
- **Campaign content:** `~/.lore/campaigns/<name>/{areas,npcs,groups,objects}/`
- **Config:** `~/.lore/config.json`

The `ensure_content_dir()` function creates the global content directory and subdirectories on first run.

## CLI Commands

### `lore tui`
Launches the interactive Textual TUI application.

### `lore display <name>`
Display a lore entry by name. Supports `--type` filter and `--raw` output.

### `lore areas`
List all area entries with tags.

### `lore npcs`
List all NPC entries with roles and tags.

### `lore groups`
List all group entries.

### `lore objects`
List all object entries.

### `lore roll [sides]`
Roll a dice (default d20).

### `lore help`
Show available commands.

## TUI (Textual)

### Layout

```
+--------+--------------------------------------+
| LORE   |                                      |
|--------|   Entry Detail View                  |
| [Buttons]                                    |
| Search   |   (content, variants, tags)        |
| [List]   |                                      |
|         |                                      |
+--------+--------------------------------------+
```

- **Sidebar:** 30 chars wide, contains title, category buttons, search input, entry list
- **Content pane:** Flexible width, displays selected entry details

### Keybindings

| Key | Action |
|-----|--------|
| `q` | Quit |
| `Esc` | Go back to list |
| `/` | Focus search input |
| `1` | Filter: Areas |
| `2` | Filter: NPCs |
| `3` | Filter: Groups |
| `4` | Filter: Objects |
| `0` | Show all |
| Arrow keys | Navigate list |
| `Enter` | Select entry |

### Category Filtering

Five buttons: All, Areas, NPCs, Groups, Objects
- Click or use keyboard shortcut `1-4`, `0`
- Updates the entry list in real-time

### Search

- Real-time filtering on name and tags (case-insensitive substring match)
- Triggered on input change
- Clears when search is emptied

### Entry Display

Shows: type icon, name, tags, full markdown content, and variants in boxed panels.

## Dependencies

```
typer>=0.12.0
python-frontmatter>=1.0.0
pyyaml>=6.0
rich>=13.0
markdown>=3.5
```

Dev dependencies: `pytest>=8.0`, `pytest-cov>=4.0`

Textual is not listed in pyproject.toml dependencies but is required for the TUI (`pip show textual` shows v8.2.8 installed).

## Sample Content

11 entries are stored in `~/.lore/content/`:

| Type | Name | Tags |
|------|------|------|
| area | The Whispering Forest | forest, dangerous, magical, ancient |
| area | Ironhaven Market | city, market, trade, bustling |
| area | Shadowfen Swamp | swamp, dangerous, undead, cursed |
| npc | Garrick the Smith | blacksmith, friendly, quest-giver, craftsman |
| npc | Old Marcus | merchant, friendly, wise, trader |
| npc | Captain Elara Voss | guard, leader, serious, quest-giver |
| group | City Watch | guards, city, lawful, military |
| group | The Silver Circle | mages, secret, magical, powerful |
| object | Dragon Slayer | weapon, legendary, magical, sword |
| object | Greater Healing Potion | consumable, healing, alchemical, potion |
| object | Map of the Forgotten Realm | treasure, knowledge, magical, map |
