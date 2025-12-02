"""Test configuration and utilities."""

import pytest


@pytest.mark.unit
def test_config_loads():
    """Test that config loads correctly."""
    from greenmining.config import Config

    config = Config()
    assert config.MAX_REPOS == 100
    assert config.COMMITS_PER_REPO == 50
    assert hasattr(config, "GITHUB_TOKEN")


@pytest.mark.unit
def test_utils_functions():
    """Test utility functions."""
    import tempfile

    # Test save and load
    from pathlib import Path

    from greenmining.utils import load_json_file, save_json_file

    test_data = {"test": "data", "count": 42}

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.json"
        save_json_file(test_data, filepath)
        loaded_data = load_json_file(filepath)

        assert loaded_data == test_data
