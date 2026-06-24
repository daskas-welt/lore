export interface LoreEntry {
  name: string;
  type: 'area' | 'npc' | 'group';
  tags?: string[];
  description: string;
  variants?: Record<string, string>;
}
