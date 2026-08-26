# Lore

A fast CLI tool for Dungeon Masters to retrieve read-aloud descriptions of areas, NPCs, and objects.

## Installation

```bash
# Install from source
pip install -e .

# Or install directly
pip install -e /path/to/lore
```

### Development

```bash
pip install -e ".[dev]"
```

## Usage

### Campaign Management

```bash
# Create a new campaign
lore init "my-campaign"

# List all campaigns
lore campaigns

# Switch active campaign
lore use my-campaign
```

### Display Content

```bash
# Display any lore entry by name
lore display forest
lore display "The Whispering Forest"

# Display specific types
lore display merchant --type npc
lore display sword --type object
```

### Scenes

```bash
# List all scenes in active campaign
lore scenes

# Display a scene
lore display forest
```

### NPCs

```bash
# List all NPCs
lore npcs

# Filter by role
lore npcs --role merchant

# Show NPC by name
lore npc "Old Marcus"
lore npc marcus
```

### Objects

```bash
# List all objects
lore objects

# Filter by category
lore objects --category weapon

# Show object by name
lore object "Dragon Slayer"
lore object sword
```

## Campaign Structure

Campaigns are stored in `~/.lore/campaigns/`:

```
~/.lore/
├── config.json              # Active campaign state
└── campaigns/
    ├── my-campaign/
    │   ├── areas/
    │   │   └── forest.md
    │   ├── npcs/
    │   │   └── merchant.md
    │   ├── groups/
    │   │   └── guards.md
    │   └── objects/
    │       └── magic-sword.md
    └── another-campaign/
        └── ...
```

## Content Format

Lore supports YAML and Markdown with YAML frontmatter.

### Markdown + Frontmatter

```markdown
---
title: "The Whispering Forest"
type: area
tags: [forest, dangerous, magical]
---

# The Whispering Forest

The trees here are ancient, their bark gnarled and silver-grey.

**Atmosphere**: Eerie silence, cold wind, strange whispers

**Key Features**:
- Towering oak trees
- Dappled sunlight
- Hidden paths between trunks
```

### YAML Format

```yaml
name: "Old Marcus"
type: npc
role: merchant
tags: [friendly, wise]
description: |
  A wizened merchant with a knowing smile.
variants:
  happy: "Ah, welcome back!"
  grumpy: "What do you want?"
```

### Frontmatter Fields

- `title` / `name` — display title (required)
- `type` — category: `area`, `npc`, `group`, `object` (required)
- `tags` — optional labels for filtering
- `variants` — optional keyed overrides (mood, time of day, etc.)

## Quick Start

```bash
# Install
pip install -e .

# Create your first campaign
lore init "my-adventure"

# Add content (create .md files in ~/.lore/campaigns/my-adventure/)
# areas/forest.md, npcs/merchant.md, objects/sword.md

# Display content during your session
lore display forest
lore npc merchant
lore objects

# Switch between campaigns
lore use other-campaign
lore campaigns
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run specific tests
pytest tests/unit/
pytest tests/integration/
```

## Commands

| Command | Description |
|---------|-------------|
| `lore init <name>` | Create a new campaign |
| `lore campaigns` | List all campaigns |
| `lore use <campaign>` | Switch active campaign |
| `lore display <name>` | Display any lore entry |
| `lore scenes` | List scenes in active campaign |
| `lore npc <name>` | Show NPC by name |
| `lore npcs` | List all NPCs |
| `lore object <name>` | Show object by name |
| `lore objects` | List all objects |
