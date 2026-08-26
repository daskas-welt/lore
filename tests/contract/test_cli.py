"""Contract tests for the Lore CLI."""

import pytest
from typer.testing import CliRunner

from lore.cli import app

runner = CliRunner()


def test_help():
    """Test --help shows usage."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Dungeon Masters" in result.output


def test_version():
    """Test --version shows version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "2.0.0" in result.output


def test_display_no_active_campaign():
    """Test display fails gracefully when no active campaign."""
    # This test requires mocking the config, so it's more of a smoke test
    result = runner.invoke(app, ["display", "test"])
    # Should fail because no active campaign is set
    assert result.exit_code != 0


def test_campaigns_no_dir():
    """Test campaigns works when no campaigns dir exists."""
    result = runner.invoke(app, ["campaigns"])
    # Should show no campaigns
    assert result.exit_code == 0
