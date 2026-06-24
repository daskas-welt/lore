import React, { useState, useMemo, useCallback } from 'react';
import { Box, Text, useInput, useStdout, useApp } from 'ink';
import Fuse from 'fuse.js';
import cfonts from 'cfonts';
import type { LoreEntry } from './core/types.js';

type Mode = 'search' | 'view';

interface AppProps {
  entries: LoreEntry[];
}

// Helper: render text with white background, padded to exact width
function BgLine({
  children,
  width,
  bold: isBold = false,
  color = 'black',
}: {
  children: React.ReactNode;
  width: number;
  bold?: boolean;
  color?: string;
}) {
  return (
    <Text bold={isBold} color={color} backgroundColor="white">
      {String(children).padEnd(width)}
    </Text>
  );
}

function BgCenter({
  text,
  width,
  bold: isBold = false,
  color = 'black',
}: {
  text: string;
  width: number;
  bold?: boolean;
  color?: string;
}) {
  const pad = Math.max(0, width - text.length);
  const left = Math.floor(pad / 2);
  const right = pad - left;
  const line = ' '.repeat(left) + text + ' '.repeat(right);
  return (
    <Text bold={isBold} color={color} backgroundColor="white">
      {line}
    </Text>
  );
}

export default function App({ entries }: AppProps) {
  const { exit } = useApp();
  const { stdout } = useStdout();
  const termWidth = stdout.columns || 80;
  const termHeight = stdout.rows || 24;

  const [mode, setMode] = useState<Mode>('search');
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [currentEntry, setCurrentEntry] = useState<LoreEntry | null>(null);
  const [variantKey, setVariantKey] = useState<string | undefined>(undefined);

  const fuse = useMemo(
    () => new Fuse(entries, { keys: ['name', 'type', 'tags'], threshold: 0.4 }),
    [entries]
  );

  const filtered = useMemo(() => {
    if (!query.trim()) return entries;
    return fuse.search(query).map((r) => r.item);
  }, [query, fuse, entries]);

  const selectEntry = useCallback((entry: LoreEntry) => {
    setCurrentEntry(entry);
    setVariantKey(undefined);
    setMode('view');
  }, []);

  useInput((input, key) => {
    if (mode === 'search') {
      if (key.return && filtered.length > 0) {
        selectEntry(filtered[selectedIndex]);
        setSelectedIndex(0);
      } else if (key.upArrow) {
        setSelectedIndex((i) => Math.max(0, i - 1));
      } else if (key.downArrow) {
        setSelectedIndex((i) => Math.min(filtered.length - 1, i + 1));
      } else if (key.backspace || key.delete) {
        setQuery((q) => q.slice(0, -1));
        setSelectedIndex(0);
      } else if (input && !key.ctrl && !key.meta && input.length === 1) {
        setQuery((q) => q + input);
        setSelectedIndex(0);
      } else if (key.escape) {
        exit();
      }
    } else if (mode === 'view') {
      if (key.escape || input === 'q') {
        setMode('search');
        setVariantKey(undefined);
      } else if (input === 'n') {
        const idx = entries.findIndex((e) => e === currentEntry);
        if (idx >= 0 && idx < entries.length - 1) {
          setCurrentEntry(entries[idx + 1]);
          setVariantKey(undefined);
        }
      } else if (input === 'p') {
        const idx = entries.findIndex((e) => e === currentEntry);
        if (idx > 0) {
          setCurrentEntry(entries[idx - 1]);
          setVariantKey(undefined);
        }
      } else if (input === 'v') {
        if (currentEntry?.variants) {
          const keys = Object.keys(currentEntry.variants);
          if (keys.length > 0) {
            const idx = variantKey ? keys.indexOf(variantKey) : -1;
            const next = keys[(idx + 1) % keys.length];
            setVariantKey(next);
          }
        }
      } else if (/^[1-9]$/.test(input) && currentEntry?.variants) {
        const keys = Object.keys(currentEntry.variants);
        const idx = parseInt(input, 10) - 1;
        if (idx < keys.length) {
          setVariantKey(keys[idx]);
        }
      }
    }
  });

  const marginX = 6;
  const paddingX = 4;
  const boxWidth = Math.max(40, termWidth - marginX * 2);
  const innerWidth = boxWidth - paddingX * 2 - 2;

  function wrapLines(text: string, width: number): string[] {
    const normalized = text.replace(/\s+/g, ' ').trim();
    const lines: string[] = [];
    let current = '';
    for (const word of normalized.split(' ')) {
      if ((current + ' ' + word).length > width) {
        lines.push(current.trim());
        current = word;
      } else {
        current = current ? current + ' ' + word : word;
      }
    }
    if (current) lines.push(current.trim());
    return lines;
  }

  // Search mode UI
  if (mode === 'search') {
    const loreHeaderResult = cfonts.render('LORE', {
      font: 'block',
      colors: ['black'],
      space: false,
    });
    const loreHeader = typeof loreHeaderResult === 'object' ? loreHeaderResult.string : 'LORE';
    const headerLines = loreHeader.split('\n');

    return (
      <Box
        flexDirection="column"
        width={termWidth}
        height={termHeight}
        alignItems="center"
        justifyContent="center"
      >
        {/* Large ASCII header */}
        <Box marginBottom={2} flexDirection="column" alignItems="center">
          {headerLines.map((line: string, i: number) => (
            <Text key={`hdr-${i}`} bold color="black">
              {line}
            </Text>
          ))}
        </Box>

        {/* Top border */}
        <Box>
          <Text color="black">{'╔' + '═'.repeat(boxWidth - 2) + '╗'}</Text>
        </Box>

        {/* Empty padding line */}
        <Box>
          <Text color="black">{'║'}</Text>
          <BgLine width={boxWidth - 2}>{''}</BgLine>
          <Text color="black">{'║'}</Text>
        </Box>

        {/* Hint */}
        <Box>
          <Text color="black">{'║'}</Text>
          <BgCenter text="Type to search, Enter to select, Esc to quit" width={boxWidth - 2} />
          <Text color="black">{'║'}</Text>
        </Box>

        {/* Empty line */}
        <Box>
          <Text color="black">{'║'}</Text>
          <BgLine width={boxWidth - 2}>{''}</BgLine>
          <Text color="black">{'║'}</Text>
        </Box>

        {/* Search prompt */}
        <Box>
          <Text color="black">{'║'}</Text>
          <BgLine width={boxWidth - 2} bold>
            {'> ' + query + '█'}
          </BgLine>
          <Text color="black">{'║'}</Text>
        </Box>

        {/* Empty line */}
        <Box>
          <Text color="black">{'║'}</Text>
          <BgLine width={boxWidth - 2}>{''}</BgLine>
          <Text color="black">{'║'}</Text>
        </Box>

        {/* Results */}
        {filtered.slice(0, 8).map((entry, i) => {
          const isSelected = i === selectedIndex;
          const label = `${isSelected ? '> ' : '  '}[${entry.type.toUpperCase()}] ${entry.name}`;
          return (
            <Box key={`${entry.type}:${entry.name}:${i}`}>
              <Text color="black">{'║'}</Text>
              {isSelected ? (
                <Text bold color="white" backgroundColor="black">
                  {label.padEnd(boxWidth - 2)}
                </Text>
              ) : (
                <BgLine width={boxWidth - 2} bold>
                  {label}
                </BgLine>
              )}
              <Text color="black">{'║'}</Text>
            </Box>
          );
        })}
        {filtered.length === 0 && (
          <Box>
            <Text color="black">{'║'}</Text>
            <BgCenter text="No matches found." width={boxWidth - 2} />
            <Text color="black">{'║'}</Text>
          </Box>
        )}

        {/* Empty line */}
        <Box>
          <Text color="black">{'║'}</Text>
          <BgLine width={boxWidth - 2}>{''}</BgLine>
          <Text color="black">{'║'}</Text>
        </Box>

        {/* Bottom border */}
        <Box>
          <Text color="black">{'╚' + '═'.repeat(boxWidth - 2) + '╝'}</Text>
        </Box>

        <Box marginTop={1}>
          <Text color="black">{filtered.length} entries</Text>
        </Box>
      </Box>
    );
  }

  // View mode UI
  if (!currentEntry) return null;

  const typeColor =
    currentEntry.type === 'area'
      ? 'cyan'
      : currentEntry.type === 'npc'
        ? 'yellow'
        : 'magenta';
  const variantKeys = currentEntry.variants ? Object.keys(currentEntry.variants) : [];

  const descLines = wrapLines(currentEntry.description, innerWidth);
  const variantLines =
    variantKey && currentEntry.variants?.[variantKey]
      ? wrapLines(currentEntry.variants[variantKey], innerWidth)
      : [];

  const contentHeight =
    2 + // top padding
    1 + // title
    (variantKey ? 1 : 0) + // variant label
    (variantKeys.length > 0 ? 1 : 0) + // variant hints
    1 + // separator
    descLines.length + // description
    (variantLines.length > 0 ? 1 + variantLines.length : 0) + // variant text
    2; // bottom padding

  const minBoxLines = Math.max(12, contentHeight);
  const fillLines = Math.max(0, minBoxLines - contentHeight);

  return (
    <Box
      flexDirection="column"
      width={termWidth}
      height={termHeight}
      alignItems="center"
      justifyContent="center"
    >
      {/* Top border */}
      <Box>
        <Text color="black">{'╔' + '═'.repeat(boxWidth - 2) + '╗'}</Text>
      </Box>

      {/* Top padding */}
      <Box>
        <Text color="black">{'║'}</Text>
        <BgLine width={boxWidth - 2}>{''}</BgLine>
        <Text color="black">{'║'}</Text>
      </Box>
      <Box>
        <Text color="black">{'║'}</Text>
        <BgLine width={boxWidth - 2}>{''}</BgLine>
        <Text color="black">{'║'}</Text>
      </Box>

      {/* Title */}
      <Box>
        <Text color="black">{'║'}</Text>
        <BgCenter
          text={`> ${currentEntry.type.toUpperCase()}: ${currentEntry.name}`}
          width={boxWidth - 2}
          bold
          color={typeColor}
        />
        <Text color="black">{'║'}</Text>
      </Box>

      {/* Variant label */}
      {variantKey && (
        <Box>
          <Text color="black">{'║'}</Text>
          <BgCenter text={`[ ${variantKey} ]`} width={boxWidth - 2} bold />
          <Text color="black">{'║'}</Text>
        </Box>
      )}

      {/* Variant hints */}
      {variantKeys.length > 0 && (
        <Box>
          <Text color="black">{'║'}</Text>
          <BgCenter
            text={'Variants: ' + variantKeys.map((k, i) => `${i + 1}:${k}`).join('  ')}
            width={boxWidth - 2}
          />
          <Text color="black">{'║'}</Text>
        </Box>
      )}

      {/* Separator */}
      <Box>
        <Text color="black">{'║'}</Text>
        <BgCenter text={'─'.repeat(Math.max(10, innerWidth - 4))} width={boxWidth - 2} />
        <Text color="black">{'║'}</Text>
      </Box>

      {/* Description */}
      {descLines.map((line, i) => (
        <Box key={`desc-${i}`}>
          <Text color="black">{'║'}</Text>
          <BgCenter text={line} width={boxWidth - 2} bold />
          <Text color="black">{'║'}</Text>
        </Box>
      ))}

      {/* Variant text */}
      {variantLines.length > 0 && (
        <>
          <Box>
            <Text color="black">{'║'}</Text>
            <BgCenter text={'─'.repeat(Math.max(10, innerWidth - 4))} width={boxWidth - 2} />
            <Text color="black">{'║'}</Text>
          </Box>
          {variantLines.map((line, i) => (
            <Box key={`var-${i}`}>
              <Text color="black">{'║'}</Text>
              <BgCenter text={line} width={boxWidth - 2} bold />
              <Text color="black">{'║'}</Text>
            </Box>
          ))}
        </>
      )}

      {/* Bottom padding */}
      <Box>
        <Text color="black">{'║'}</Text>
        <BgLine width={boxWidth - 2}>{''}</BgLine>
        <Text color="black">{'║'}</Text>
      </Box>
      <Box>
        <Text color="black">{'║'}</Text>
        <BgLine width={boxWidth - 2}>{''}</BgLine>
        <Text color="black">{'║'}</Text>
      </Box>

      {/* Fill remaining space */}
      {Array.from({ length: fillLines }).map((_, i) => (
        <Box key={`fill-${i}`}>
          <Text color="black">{'║'}</Text>
          <BgLine width={boxWidth - 2}>{''}</BgLine>
          <Text color="black">{'║'}</Text>
        </Box>
      ))}

      {/* Bottom border */}
      <Box>
        <Text color="black">{'╚' + '═'.repeat(boxWidth - 2) + '╝'}</Text>
      </Box>

      {/* Controls footer */}
      <Box marginTop={2} alignItems="center">
        <Text color="black">
          q/Esc: back · n/p: next/prev · v: cycle variant · 1-9: select variant
        </Text>
      </Box>
    </Box>
  );
}
