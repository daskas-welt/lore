"""Data models for Lore entries and campaigns."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


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


@dataclass
class Campaign:
    """A campaign directory containing lore entries."""

    name: str
    path: Path
    created: str = ""
    last_accessed: str = ""

    def exists(self) -> bool:
        return self.path.exists() and self.path.is_dir()


@dataclass
class Config:
    """Global configuration stored in ~/.lore/config.json."""

    active_campaign: Optional[str] = None
    campaigns_path: str = ""
    version: str = "2.0.0"
    preferences: dict = field(default_factory=dict)
