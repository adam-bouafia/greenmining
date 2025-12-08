"""Tests for enhanced statistics in report generation."""

import pytest

from greenmining.services.reports import ReportGenerator


class TestEnhancedReportGeneration:
    """Test enhanced statistics section in reports."""

    def test_enhanced_statistics_section_with_data(self):
        """Test enhanced statistics section generates correctly with valid data."""
        generator = ReportGenerator()

        # Sample enhanced statistics data
        data = {
            "summary": {
                "total_commits": 1000,
                "green_aware_count": 150,
                "green_aware_percentage": 15.0,
                "total_repos": 50,
                "repos_with_green_commits": 30,
            },
            "enhanced_statistics": {
                "temporal_trends": {
                    "overall_trend": {"direction": "increasing", "significant": True},
                    "monthly_stats": {"mean": 25.5, "median": 23.0, "std": 8.2},
                },
                "pattern_correlations": {
                    "top_positive_correlations": [
                        {"pattern1": "caching", "pattern2": "performance", "correlation": 0.75}
                    ]
                },
                "effect_size": {
                    "green_vs_nongreen_patterns": {"cohens_d": 0.65, "magnitude": "medium"}
                },
                "descriptive": {
                    "patterns_per_commit": {"mean": 2.3, "median": 2.0, "std": 1.1},
                    "green_commits_per_repo": {"mean": 15.0, "median": 12.0, "std": 8.5},
                },
            },
            "known_patterns": [],
            "emergent_patterns": [],
            "per_repo_stats": [],
        }

        section = generator._generate_enhanced_statistics_section(data)

        assert section != ""
        assert "#### 2.5 Enhanced Statistical Analysis" in section
        assert "##### Temporal Trends" in section
        assert "increasing" in section.lower()
        assert "##### Pattern Correlations" in section
        assert "caching" in section
        assert "##### Effect Size Analysis" in section
        assert "0.65" in section
        assert "##### Descriptive Statistics" in section

    def test_enhanced_statistics_section_no_data(self):
        """Test enhanced statistics section returns empty when no data."""
        generator = ReportGenerator()

        data = {"summary": {}, "known_patterns": [], "emergent_patterns": [], "per_repo_stats": []}

        section = generator._generate_enhanced_statistics_section(data)

        assert section == ""

    def test_enhanced_statistics_section_with_error(self):
        """Test enhanced statistics section handles errors gracefully."""
        generator = ReportGenerator()

        data = {
            "summary": {},
            "enhanced_statistics": {"error": "Insufficient data for statistical analysis"},
            "known_patterns": [],
            "emergent_patterns": [],
            "per_repo_stats": [],
        }

        section = generator._generate_enhanced_statistics_section(data)

        assert section != ""
        assert "#### 2.5 Enhanced Statistical Analysis" in section
        assert "error" in section.lower()
        assert "Insufficient data" in section

    def test_results_section_includes_enhanced_stats(self):
        """Test results section includes enhanced statistics when available."""
        generator = ReportGenerator()

        data = {
            "summary": {
                "total_commits": 1000,
                "green_aware_count": 150,
                "green_aware_percentage": 15.0,
                "total_repos": 50,
                "repos_with_green_commits": 30,
            },
            "enhanced_statistics": {
                "temporal_trends": {"overall_trend": {"direction": "stable", "significant": False}}
            },
            "known_patterns": [],
            "emergent_patterns": [],
            "per_repo_stats": [],
            "per_language_stats": {},
        }

        results = generator._generate_results(data)

        assert "### 2. Results" in results
        assert "#### 2.5 Enhanced Statistical Analysis" in results

    def test_results_section_without_enhanced_stats(self):
        """Test results section works without enhanced statistics."""
        generator = ReportGenerator()

        data = {
            "summary": {
                "total_commits": 1000,
                "green_aware_count": 150,
                "green_aware_percentage": 15.0,
                "total_repos": 50,
                "repos_with_green_commits": 30,
            },
            "known_patterns": [],
            "emergent_patterns": [],
            "per_repo_stats": [],
            "per_language_stats": {},
        }

        results = generator._generate_results(data)

        assert "### 2. Results" in results
        assert "#### 2.5 Enhanced Statistical Analysis" not in results
