"""Unit tests for the config module."""

import pytest
from pathlib import Path

from lore.core.config import CONTENT_DIR, get_content_path, ensure_content_dir


class TestContentPath:
    """Test content path configuration."""

    def test_content_dir_is_path(self):
        assert isinstance(CONTENT_DIR, Path)

    def test_content_dir_ends_with_content(self):
        assert CONTENT_DIR.name == "content"

    def test_content_dir_inside_lore_dir(self):
        assert CONTENT_DIR.parent.name == ".lore"

    def test_get_content_path_returns_same_dir(self):
        assert get_content_path() == CONTENT_DIR

    def test_get_content_path_returns_path(self):
        assert isinstance(get_content_path(), Path)
