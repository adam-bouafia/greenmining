"""Tests for Code Diff Analyzer."""

import pytest
from unittest.mock import Mock
from greenmining.analyzers.code_diff_analyzer import CodeDiffAnalyzer


class TestCodeDiffAnalyzer:
    """Test suite for CodeDiffAnalyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return CodeDiffAnalyzer()

    def test_detect_caching_pattern(self, analyzer):
        """Test detection of caching patterns in code."""
        code_line = "from functools import lru_cache"
        patterns = analyzer._detect_patterns_in_line(code_line)
        assert "caching" in patterns

    def test_detect_resource_optimization(self, analyzer):
        """Test detection of resource optimization patterns."""
        code_line = "resources: limits:"
        patterns = analyzer._detect_patterns_in_line(code_line)
        assert "resource_optimization" in patterns

    def test_detect_async_processing(self, analyzer):
        """Test detection of async processing patterns."""
        code_line = "async def process_data():"
        patterns = analyzer._detect_patterns_in_line(code_line)
        assert "async_processing" in patterns

    def test_calculate_metrics(self, analyzer):
        """Test code change metrics calculation."""
        # Create mock commit
        mock_commit = Mock()
        mock_file1 = Mock()
        mock_file1.added_lines = 10
        mock_file1.deleted_lines = 5
        mock_file1.complexity = 2

        mock_file2 = Mock()
        mock_file2.added_lines = 15
        mock_file2.deleted_lines = 3
        mock_file2.complexity = 3

        mock_commit.modified_files = [mock_file1, mock_file2]

        metrics = analyzer._calculate_metrics(mock_commit)

        assert metrics["lines_added"] == 25
        assert metrics["lines_removed"] == 8
        assert metrics["files_changed"] == 2
        assert metrics["net_lines"] == 17

    def test_is_code_file_python(self, analyzer):
        """Test identification of Python code files."""
        mock_file = Mock()
        mock_file.filename = "test.py"
        assert analyzer._is_code_file(mock_file) is True

    def test_is_code_file_dockerfile(self, analyzer):
        """Test identification of Dockerfile."""
        mock_file = Mock()
        mock_file.filename = "Dockerfile"
        assert analyzer._is_code_file(mock_file) is True

    def test_is_code_file_non_code(self, analyzer):
        """Test rejection of non-code files."""
        mock_file = Mock()
        mock_file.filename = "README.md"
        mock_file.source_code = None
        assert analyzer._is_code_file(mock_file) is False

    def test_confidence_high(self, analyzer):
        """Test high confidence calculation."""
        patterns = ["caching", "async_processing", "resource_optimization"]
        evidence = {
            "caching": ["line1", "line2"],
            "async_processing": ["line3", "line4"],
            "resource_optimization": ["line5"],
        }
        metrics = {"lines_added": 20}

        confidence = analyzer._calculate_diff_confidence(patterns, evidence, metrics)
        assert confidence == "high"

    def test_confidence_medium(self, analyzer):
        """Test medium confidence calculation."""
        patterns = ["caching", "async_processing"]
        evidence = {"caching": ["line1", "line2"], "async_processing": ["line3"]}
        metrics = {"lines_added": 10}

        confidence = analyzer._calculate_diff_confidence(patterns, evidence, metrics)
        assert confidence == "medium"

    def test_confidence_low(self, analyzer):
        """Test low confidence calculation."""
        patterns = ["caching"]
        evidence = {"caching": ["line1"]}
        metrics = {"lines_added": 5}

        confidence = analyzer._calculate_diff_confidence(patterns, evidence, metrics)
        assert confidence == "low"

    def test_confidence_none(self, analyzer):
        """Test no confidence when no patterns detected."""
        patterns = []
        evidence = {}
        metrics = {"lines_added": 0}

        confidence = analyzer._calculate_diff_confidence(patterns, evidence, metrics)
        assert confidence == "none"
