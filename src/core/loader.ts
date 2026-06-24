import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import type { LoreEntry } from './types.js';

const VALID_TYPES = new Set(['area', 'npc', 'group']);

function isValidEntry(obj: unknown): obj is LoreEntry {
  if (typeof obj !== 'object' || obj === null) return false;
  const e = obj as Record<string, unknown>;
  if (typeof e.name !== 'string') return false;
  if (typeof e.type !== 'string' || !VALID_TYPES.has(e.type)) return false;
  if (typeof e.description !== 'string') return false;
  return true;
}

export function loadLoreFile(filePath: string): LoreEntry[] {
  const content = fs.readFileSync(filePath, 'utf-8');
  const ext = path.extname(filePath).toLowerCase();
  let data: unknown;

  if (ext === '.yaml' || ext === '.yml') {
    data = yaml.load(content);
  } else if (ext === '.json') {
    data = JSON.parse(content);
  } else {
    throw new Error(`Unsupported file extension: ${ext}`);
  }

  const entries: LoreEntry[] = [];
  const docs = Array.isArray(data) ? data : [data];

  for (const doc of docs) {
    if (isValidEntry(doc)) {
      entries.push(doc);
    } else {
      console.warn(`Skipping invalid lore file entry in ${filePath}`);
    }
  }

  return entries;
}

export function loadLoreDir(dirPath: string): LoreEntry[] {
  const entries: LoreEntry[] = [];

  function recurse(current: string) {
    const items = fs.readdirSync(current);
    for (const item of items) {
      const full = path.join(current, item);
      const stat = fs.statSync(full);
      if (stat.isDirectory()) {
        recurse(full);
      } else {
        const ext = path.extname(item).toLowerCase();
        if (ext === '.yaml' || ext === '.yml' || ext === '.json') {
          entries.push(...loadLoreFile(full));
        }
      }
    }
  }

  recurse(dirPath);
  return entries;
}

export function findLoreDir(): string {
  const cwd = process.cwd();
  const localLore = path.join(cwd, 'lore');

  if (fs.existsSync(localLore) && fs.statSync(localLore).isDirectory()) {
    return localLore;
  }

  const __dirname = path.dirname(new URL(import.meta.url).pathname);
  const builtin = path.resolve(__dirname, '..', '..', 'lore');
  if (fs.existsSync(builtin) && fs.statSync(builtin).isDirectory()) {
    return builtin;
  }

  throw new Error('Could not find a lore directory. Create one in your current working directory.');
}
