"""Tests for Enhanced Statistical Analyzer."""

import pytest
import pandas as pd
import numpy as np
from greenmining.analyzers.statistical_analyzer import EnhancedStatisticalAnalyzer


class TestEnhancedStatisticalAnalyzer:
    """Test suite for EnhancedStatisticalAnalyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return EnhancedStatisticalAnalyzer()

    @pytest.fixture
    def sample_commit_data(self):
        """Create sample commit data for testing."""
        return pd.DataFrame(
            {
                "commit_hash": ["a1", "a2", "a3", "a4", "a5"],
                "date": pd.to_datetime(
                    ["2023-01-01", "2023-02-01", "2023-03-01", "2023-04-01", "2023-05-01"]
                ),
                "green_aware": [1, 0, 1, 1, 0],
                "pattern_caching": [1, 0, 1, 0, 0],
                "pattern_async": [0, 0, 1, 1, 0],
            }
        )

    def test_pattern_correlations(self, analyzer, sample_commit_data):
        """Test pattern correlation analysis."""
        result = analyzer.analyze_pattern_correlations(sample_commit_data)

        assert "correlation_matrix" in result
        assert "significant_pairs" in result
        assert "interpretation" in result

    def test_temporal_trend_analysis(self, analyzer, sample_commit_data):
        """Test temporal trend analysis."""
        result = analyzer.temporal_trend_analysis(sample_commit_data)

        assert "trend" in result
        assert "direction" in result["trend"]
        assert result["trend"]["direction"] in ["increasing", "decreasing"]
        assert "significant" in result["trend"]
        assert isinstance(result["trend"]["significant"], bool)

    def test_effect_size_analysis(self, analyzer):
        """Test effect size analysis."""
        group1 = [0.5, 0.6, 0.7, 0.8, 0.9]
        group2 = [0.2, 0.3, 0.4, 0.5, 0.6]

        result = analyzer.effect_size_analysis(group1, group2)

        assert "cohens_d" in result
        assert "magnitude" in result
        assert "mean_difference" in result
        assert "p_value" in result
        assert "significant" in result

        assert result["magnitude"] in ["negligible", "small", "medium", "large"]
        assert isinstance(result["significant"], bool)

    def test_effect_size_equal_groups(self, analyzer):
        """Test effect size with equal groups."""
        group1 = [0.5, 0.5, 0.5, 0.5, 0.5]
        group2 = [0.5, 0.5, 0.5, 0.5, 0.5]

        result = analyzer.effect_size_analysis(group1, group2)

        assert result["cohens_d"] == 0
        assert result["magnitude"] == "negligible"
        assert result["mean_difference"] == 0

    def test_pattern_adoption_rate_analysis(self, analyzer):
        """Test pattern adoption rate analysis."""
        data = pd.DataFrame(
            {
                "pattern": ["caching", "caching", "async", "async", "caching"],
                "date": pd.to_datetime(
                    ["2023-01-01", "2023-02-01", "2023-01-15", "2023-03-01", "2023-04-01"]
                ),
            }
        )

        result = analyzer.pattern_adoption_rate_analysis(data)

        assert "caching" in result
        assert "async" in result

        assert "ttfa_days" in result["caching"]
        assert "total_adoptions" in result["caching"]
        assert result["caching"]["total_adoptions"] == 3

        assert "total_adoptions" in result["async"]
        assert result["async"]["total_adoptions"] == 2

    def test_interpret_correlations(self, analyzer):
        """Test correlation interpretation."""
        pairs = [
            {
                "pattern1": "pattern_caching",
                "pattern2": "pattern_async",
                "correlation": 0.85,
                "strength": "strong",
            }
        ]

        interpretation = analyzer._interpret_correlations(pairs)

        assert "caching" in interpretation
        assert "async" in interpretation
        assert "adopted together" in interpretation

    def test_interpret_correlations_empty(self, analyzer):
        """Test correlation interpretation with no pairs."""
        interpretation = analyzer._interpret_correlations([])

        assert "No significant correlations" in interpretation
