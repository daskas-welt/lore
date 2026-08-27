"""Data models for Lore entries."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LoreEntry:
    """A single lore entry (area, npc, group, or object)."""

    name: str
    type: str  # 'area', 'npc', 'group', 'object'
    tags: list[str] = field(default_factory=list)
    path: Path = field(default_factory=lambda: Path())
    content: str = ""
    frontmatter: dict = field(default_factory=dict)
    variants: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if self.type not in ("area", "npc", "group", "object"):
            raise ValueError(
                f"Invalid type: {self.type}. Must be area, npc, group, or object"
            )
