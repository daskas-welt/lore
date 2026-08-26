"""ANSI rendering for markdown content."""

import re
from typing import Optional


def render_markdown_to_ansi(content: str) -> str:
    """Convert markdown text to ANSI-formatted terminal output."""
    if not content:
        return ""

    lines = content.split("\n")
    output_lines = []

    for line in lines:
        rendered = _render_line(line)
        output_lines.append(rendered)

    return "\n".join(output_lines)


def _render_line(line: str) -> str:
    """Render a single markdown line to ANSI."""
    # Headers: # Header -> bold
    if line.startswith("######"):
        return f"\033[1m{line[6:].strip()}\033[0m"
    elif line.startswith("#####"):
        return f"\033[1m{line[5:].strip()}\033[0m"
    elif line.startswith("####"):
        return f"\033[1m{line[4:].strip()}\033[0m"
    elif line.startswith("###"):
        return f"\033[1m{line[3:].strip()}\033[0m"
    elif line.startswith("##"):
        return f"\033[1m{line[2:].strip()}\033[0m"
    elif line.startswith("#"):
        return f"\033[1m{line[1:].strip()}\033[0m"

    # Horizontal rule
    if re.match(r"^[-*_]{3,}$", line.strip()):
        return "─" * 40

    # List items: - item or * item or 1. item
    list_match = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", line)
    if list_match:
        indent, bullet, text = list_match.groups()
        rendered_text = _render_inline(text)
        if bullet in ("-", "*"):
            return f"{indent}• {rendered_text}"
        else:
            return f"{indent}{bullet} {rendered_text}"

    # Blockquote
    if line.startswith(">"):
        return f"\033[2m{line}\033[0m"

    # Regular paragraph - render inline formatting
    return _render_inline(line)


def _render_inline(text: str) -> str:
    """Render inline markdown formatting to ANSI."""
    # Bold: **text** or __text__
    text = re.sub(
        r"\*\*(.+?)\*\*",
        lambda m: f"\033[1m{m.group(1)}\033[0m",
        text,
    )
    text = re.sub(
        r"__(.+?)__",
        lambda m: f"\033[1m{m.group(1)}\033[0m",
        text,
    )

    # Italic: *text* or _text_
    text = re.sub(
        r"\*(.+?)\*",
        lambda m: f"\033[3m{m.group(1)}\033[0m",
        text,
    )
    text = re.sub(
        r"(?<!\w)_(.+?)_(?!\w)",
        lambda m: f"\033[3m{m.group(1)}\033[0m",
        text,
    )

    # Code: `text`
    text = re.sub(
        r"`(.+?)`",
        lambda m: f"\033[7m{m.group(1)}\033[0m",
        text,
    )

    # Strikethrough: ~~text~~
    text = re.sub(
        r"~~(.+?)~~",
        lambda m: f"\033[9m{m.group(1)}\033[0m",
        text,
    )

    return text


def format_entry_header(name: str, entry_type: str, tags: list[str]) -> str:
    """Format an entry header with type and tags."""
    header = f"\033[1m{entry_type.upper()}: {name}\033[0m"
    if tags:
        header += f" [{', '.join(tags)}]"
    return header


def format_entry_content(content: str, variants: Optional[dict] = None) -> str:
    """Format entry content with optional variant selection."""
    output = render_markdown_to_ansi(content)

    if variants:
        output += "\n\n"
        for key, value in variants.items():
            output += f"\033[1m{key.title()}:\033[0m\n"
            output += render_markdown_to_ansi(value)
            output += "\n"

    return output
