"""Integration tests for campaign commands."""

import tempfile
import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from lore.cli import app

runner = CliRunner()


@pytest.fixture
def temp_campaigns_dir(monkeypatch):
    """Create a temporary campaigns directory."""
    temp_dir = Path(tempfile.mkdtemp())
    monkeypatch.setattr("lore.core.config.CAMPAIGNS_DIR", temp_dir)
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_init_campaign(temp_campaigns_dir):
    """Test creating a new campaign."""
    result = runner.invoke(app, ["init", "test-campaign"])

    assert result.exit_code == 0
    assert (temp_campaigns_dir / "test-campaign").exists()
    assert (temp_campaigns_dir / "test-campaign" / "areas").exists()
    assert (temp_campaigns_dir / "test-campaign" / "npcs").exists()
    assert (temp_campaigns_dir / "test-campaign" / "groups").exists()
    assert (temp_campaigns_dir / "test-campaign" / "objects").exists()


def test_list_campaigns_empty(temp_campaigns_dir):
    """Test listing campaigns when none exist."""
    result = runner.invoke(app, ["campaigns"])

    assert result.exit_code == 0
    assert "No campaigns found" in result.output


def test_list_campaigns(temp_campaigns_dir):
    """Test listing campaigns."""
    # Create a campaign
    (temp_campaigns_dir / "campaign-a").mkdir()
    (temp_campaigns_dir / "campaign-b").mkdir()

    result = runner.invoke(app, ["campaigns"])

    assert result.exit_code == 0
    assert "campaign-a" in result.output
    assert "campaign-b" in result.output
