"""Tests for temporal filtering functionality."""

import pytest
from unittest.mock import Mock, patch
from greenmining.controllers.repository_controller import RepositoryController
from greenmining.config import Config


class TestTemporalFiltering:
    """Test suite for temporal filtering in repository search."""

    @pytest.fixture
    def mock_config(self):
        """Create mock configuration."""
        config = Mock(spec=Config)
        config.GITHUB_TOKEN = "test_token"
        config.MAX_REPOS = 100
        config.MIN_STARS = 100
        config.SUPPORTED_LANGUAGES = ["Python", "Java"]
        config.REPOS_FILE = Mock()
        return config

    @pytest.fixture
    def controller(self, mock_config):
        """Create controller instance."""
        with patch("greenmining.controllers.repository_controller.Github"):
            return RepositoryController(mock_config)

    def test_build_temporal_query_full(self, controller):
        """Test query building with all temporal parameters."""
        query = controller._build_temporal_query(
            keywords="microservices",
            min_stars=100,
            created_after="2020-01-01",
            created_before="2023-12-31",
            pushed_after="2023-01-01",
            pushed_before="2023-12-31",
        )

        assert "microservices" in query
        assert "stars:>=100" in query
        assert "created:2020-01-01..2023-12-31" in query
        assert "pushed:2023-01-01..2023-12-31" in query

    def test_build_temporal_query_created_after_only(self, controller):
        """Test query with only created_after filter."""
        query = controller._build_temporal_query(
            keywords="microservices", min_stars=100, created_after="2020-01-01"
        )

        assert "created:>=2020-01-01" in query
        assert "pushed:" not in query

    def test_build_temporal_query_pushed_before_only(self, controller):
        """Test query with only pushed_before filter."""
        query = controller._build_temporal_query(
            keywords="microservices", min_stars=100, pushed_before="2023-12-31"
        )

        assert "pushed:<=2023-12-31" in query
        assert "created:" not in query

    def test_build_temporal_query_no_temporal(self, controller):
        """Test query without temporal filters."""
        query = controller._build_temporal_query(keywords="microservices", min_stars=100)

        assert "microservices" in query
        assert "stars:>=100" in query
        assert "created:" not in query
        assert "pushed:" not in query

    def test_build_temporal_query_keywords_format(self, controller):
        """Test query with multiple keywords."""
        query = controller._build_temporal_query(
            keywords="kubernetes docker", min_stars=50, created_after="2022-01-01"
        )

        assert "kubernetes docker" in query
        assert "stars:>=50" in query
        assert "created:>=2022-01-01" in query
