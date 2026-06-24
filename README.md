# Lore

A fast CLI tool for Dungeon Masters to retrieve read-aloud descriptions of areas, NPCs, and groups. Built with [Ink](https://github.com/vadimdemedes/ink) for a rich, full-screen terminal UI with centered text, generous padding, and retro text-adventure styling.

## Installation

```bash
npm install
npm run build
npm link
```

## Usage

### Interactive TUI (default)

```bash
lore
```

Opens a full-screen interface:
- **Type to search** — fuzzy-filter entries in real time
- **↑/↓** — highlight an entry
- **Enter** — view the selected entry

In view mode:
- **q / Esc** — back to search
- **n / p** — next / previous entry
- **v** — cycle variants
- **1-9** — jump to a specific variant

The output is centered on screen with double-line borders, generous padding, and bold green text — evoking classic text adventures.

### Non-interactive CLI

When piping or running without a TTY, Lore falls back to simple CLI output:

```bash
lore show forest
lore s garrick
lore help
```

## Content Directory

By default, Lore looks for a `lore/` directory in your current working directory. If none is found, it falls back to the built-in example content.

### Directory layout

```
lore/
├── areas/
│   └── forest.yaml
├── npcs/
│   └── blacksmith.yaml
└── groups/
    └── guards.yaml
```

### YAML Schema

```yaml
name: "The Whispering Forest"
type: area              # area | npc | group
tags: [forest, magical]
description: |
  The trees here are ancient...
variants:
  morning: |
    Golden shafts of light...
  evening: |
    Long shadows stretch...
```

- `name` — display title
- `type` — category for filtering
- `tags` — optional labels for future use
- `description` — base text, always shown
- `variants` — optional keyed overrides (time of day, weather, mood, etc.)

## Font Size

The TUI cannot change your terminal's actual font size — that's controlled by your terminal emulator. To make text larger:

- **Windows Terminal**: `Ctrl` + `+` or `Ctrl` + scroll wheel
- **CMD**: Right-click title bar → Properties → Font tab

The large ASCII "LORE" header and bold double-line borders are designed to look substantial even at default sizes.
