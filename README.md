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

### Display Content

```bash
# Display any lore entry by name
lore display forest
lore display "The Whispering Forest"

# Display specific types
lore display merchant --type npc
lore display sword --type object
```

### Areas

```bash
# List all areas
lore areas
```

### NPCs

```bash
# List all NPCs
lore npcs
```

### Groups

```bash
# List all groups
lore groups
```

### Objects

```bash
# List all objects
lore objects
```

### Dice Roll

```bash
# Roll a d20 (default)
lore roll

# Roll a d6
lore roll 6
```

## Content Structure

Content is stored in `~/.lore/content/`:

```
~/.lore/content/
├── areas/
│   └── forest.md
├── npcs/
│   └── merchant.md
├── groups/
│   └── guards.md
└── objects/
    └── magic-sword.md
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

# Add content (create .md files in ~/.lore/content/)
# areas/forest.md, npcs/merchant.md, objects/sword.md

# Display content during your session
lore display forest
lore npcs
lore objects
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
| `lore display <name>` | Display any lore entry |
| `lore areas` | List all areas |
| `lore npcs` | List all NPCs |
| `lore groups` | List all groups |
| `lore objects` | List all objects |
| `lore roll [sides]` | Roll a dice (default d20) |
| `lore help` | Show available commands |
