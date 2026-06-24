#!/usr/bin/env node
import React from 'react';
import { render } from 'ink';
import App from './app.js';
import { loadLoreDir, findLoreDir } from './core/loader.js';
import { buildRegistry, findEntry } from './core/registry.js';
import Fuse from 'fuse.js';

const loreDir = findLoreDir();
const entries = loadLoreDir(loreDir);

// If stdin is not a TTY, fall back to traditional CLI mode
if (!process.stdin.isTTY) {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === 'help' || command === '/help' || command === 'h') {
    console.log(`
LORE — DM Command Reference

lore                    Launch interactive TUI
lore show <type> <name> Show a lore entry
lore s <name>           Show entry (search all types)

Examples:
  lore s area forest
  lore s forest
  lore s garrick
`);
    process.exit(0);
  }

  if (command === 'show' || command === 's') {
    const registry = buildRegistry(entries);
    let type: string | undefined;
    let name: string;

    if (args.length >= 3) {
      type = args[1];
      name = args[2];
    } else if (args.length >= 2) {
      name = args[1];
    } else {
      console.error('Usage: lore show <type> <name> or lore show <name>');
      process.exit(1);
    }

    let entry = findEntry(registry, name!);

    if (!entry) {
      const fuse = new Fuse(entries, { keys: ['name'], threshold: 0.4 });
      const results = fuse.search(name!);
      if (results.length > 0) entry = results[0].item;
    }

    if (!entry) {
      console.error(`No lore found for "${name}".`);
      process.exit(1);
    }

    // Simple text output for non-interactive mode
    console.log(`\n> ${entry.type.toUpperCase()}: ${entry.name}\n`);
    console.log(entry.description.trim());
    if (entry.variants) {
      console.log('\nVariants:', Object.keys(entry.variants).join(', '));
    }
    console.log();
    process.exit(0);
  }

  console.error(`Unknown command: ${command}`);
  process.exit(1);
}

// Interactive TUI mode
render(<App entries={entries} />);
