"""Unit tests for the LoreEntry model."""

import pytest
from pathlib import Path

from lore.core.models import LoreEntry


class TestLoreEntryCreation:
    """Test LoreEntry creation and validation."""

    def test_create_area_entry(self):
        entry = LoreEntry(
            name="Forest",
            type="area",
            tags=["dark", "magical"],
            path=Path("forest.md"),
            content="A dark forest.",
        )
        assert entry.name == "Forest"
        assert entry.type == "area"
        assert entry.tags == ["dark", "magical"]
        assert entry.content == "A dark forest."

    def test_create_npc_entry(self):
        entry = LoreEntry(
            name="Marcus",
            type="npc",
            tags=["merchant"],
            path=Path("marcus.md"),
            content="A wise merchant.",
        )
        assert entry.type == "npc"

    def test_create_group_entry(self):
        entry = LoreEntry(
            name="City Watch",
            type="group",
            tags=["guards"],
            path=Path("guards.md"),
            content="Blue-cloaked guards.",
        )
        assert entry.type == "group"

    def test_create_object_entry(self):
        entry = LoreEntry(
            name="Sword",
            type="object",
            tags=["weapon"],
            path=Path("sword.md"),
            content="A magical sword.",
        )
        assert entry.type == "object"

    def test_create_with_variants(self):
        variants = {"happy": "Hello!", "grumpy": "Go away."}
        entry = LoreEntry(
            name="NPC",
            type="npc",
            tags=[],
            path=Path("npc.md"),
            content="An NPC.",
            variants=variants,
        )
        assert entry.variants == variants

    def test_create_with_frontmatter(self):
        frontmatter = {"name": "Test", "type": "area", "custom_field": "value"}
        entry = LoreEntry(
            name="Test",
            type="area",
            tags=[],
            path=Path("test.md"),
            content="Content.",
            frontmatter=frontmatter,
        )
        assert entry.frontmatter == frontmatter

    def test_default_values(self):
        entry = LoreEntry(
            name="Test",
            type="area",
            tags=[],
            path=Path("test.md"),
            content="",
        )
        assert entry.variants == {}
        assert entry.frontmatter == {}

    def test_invalid_type_raises_error(self):
        with pytest.raises(ValueError, match="Invalid type"):
            LoreEntry(
                name="Test",
                type="invalid",
                tags=[],
                path=Path("test.md"),
                content="",
            )

    def test_all_valid_types(self):
        for entry_type in ("area", "npc", "group", "object"):
            entry = LoreEntry(
                name="Test",
                type=entry_type,
                tags=[],
                path=Path("test.md"),
                content="",
            )
            assert entry.type == entry_type
