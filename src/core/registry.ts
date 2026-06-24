import type { LoreEntry } from './types.js';

export function buildRegistry(entries: LoreEntry[]) {
  const byName = new Map<string, LoreEntry[]>();
  for (const entry of entries) {
    const key = entry.name.toLowerCase();
    if (!byName.has(key)) byName.set(key, []);
    byName.get(key)!.push(entry);
  }
  return { all: entries, byName };
}

export function findEntry(registry: { all: LoreEntry[] }, name: string): LoreEntry | undefined {
  const nameLower = name.toLowerCase();
  return registry.all.find((e) => e.name.toLowerCase() === nameLower);
}
