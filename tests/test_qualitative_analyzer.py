"""
Test suite for Qualitative Analyzer
"""

import pytest
import tempfile
import json
import os
from greenmining.analyzers.qualitative_analyzer import (
    QualitativeAnalyzer,
    ValidationSample,
    ValidationMetrics,
)


class TestQualitativeAnalyzer:
    """Test qualitative analysis and validation framework"""

    @pytest.fixture
    def analyzer(self):
        """Create qualitative analyzer instance"""
        return QualitativeAnalyzer(sample_size=10, stratify_by="pattern")

    @pytest.fixture
    def sample_commits(self):
        """Sample commits"""
        return [
            {"hash": f"commit{i}", "message": f"message {i}", "repository": "repo1"}
            for i in range(50)
        ]

    @pytest.fixture
    def sample_analysis_results(self):
        """Sample analysis results with patterns"""
        results = []
        patterns = ["caching", "compression", "optimization", "async"]

        for i in range(50):
            results.append(
                {
                    "commit_sha": f"commit{i}",
                    "is_green_aware": i < 30,  # 30 positives, 20 negatives
                    "patterns_detected": [patterns[i % len(patterns)]] if i < 30 else [],
                    "commit_message": f"message {i}",
                    "repository": "repo1",
                }
            )

        return results

    def test_generate_validation_samples(self, analyzer, sample_commits, sample_analysis_results):
        """Test validation sample generation"""
        samples = analyzer.generate_validation_samples(
            sample_commits, sample_analysis_results, include_negatives=True
        )

        assert len(samples) == 10
        assert all(isinstance(s, ValidationSample) for s in samples)

        # Should have mix of positives and negatives
        positives = [s for s in samples if len(s.detected_patterns) > 0]
        negatives = [s for s in samples if len(s.detected_patterns) == 0]

        assert len(positives) > 0
        assert len(negatives) > 0  # Since include_negatives=True

    def test_stratified_sample_by_pattern(self, analyzer, sample_analysis_results):
        """Test stratified sampling by pattern"""
        positives = [r for r in sample_analysis_results if r["is_green_aware"]]

        samples = analyzer._stratified_sample_by_pattern(positives, 10)

        assert len(samples) <= 10

        # Check pattern diversity
        all_patterns = set()
        for sample in samples:
            all_patterns.update(sample.get("patterns_detected", []))

        assert len(all_patterns) > 1  # Should have multiple patterns

    def test_export_samples_for_review(self, analyzer, sample_commits, sample_analysis_results):
        """Test exporting samples to JSON"""
        analyzer.generate_validation_samples(sample_commits, sample_analysis_results)

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            output_path = f.name

        try:
            analyzer.export_samples_for_review(output_path)

            # Read back and verify
            with open(output_path, "r") as f:
                data = json.load(f)

            assert len(data) == len(analyzer.samples)
            assert all("commit_sha" in item for item in data)
            assert all("detected_patterns" in item for item in data)
            assert all("___INSTRUCTIONS___" in item for item in data)
        finally:
            os.unlink(output_path)

    def test_import_validated_samples(self, analyzer, sample_commits, sample_analysis_results):
        """Test importing validated samples"""
        analyzer.generate_validation_samples(sample_commits, sample_analysis_results)

        # Create temporary validation file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            output_path = f.name

        try:
            # Export samples
            analyzer.export_samples_for_review(output_path)

            # Modify with validation
            with open(output_path, "r") as f:
                data = json.load(f)

            for item in data[:5]:  # Validate first 5
                item["true_label"] = True
                item["reviewer"] = "test_reviewer"
                item["review_notes"] = "Looks good"

            with open(output_path, "w") as f:
                json.dump(data, f)

            # Import back
            analyzer.import_validated_samples(output_path)

            # Check validation status
            validated = [s for s in analyzer.samples if s.validation_status == "validated"]
            assert len(validated) == 5
        finally:
            os.unlink(output_path)

    def test_calculate_metrics(self, analyzer):
        """Test precision/recall calculation"""
        # Create samples with known labels
        analyzer.samples = [
            ValidationSample(
                commit_sha="tp1",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["caching"],
                detection_method="keyword",
                true_label=True,
            ),
            ValidationSample(
                commit_sha="tp2",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["async"],
                detection_method="keyword",
                true_label=True,
            ),
            ValidationSample(
                commit_sha="fp1",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["caching"],
                detection_method="keyword",
                true_label=False,
            ),
            ValidationSample(
                commit_sha="tn1",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=[],
                detection_method="keyword",
                true_label=False,
            ),
            ValidationSample(
                commit_sha="fn1",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=[],
                detection_method="keyword",
                true_label=True,
            ),
        ]

        metrics = analyzer.calculate_metrics()

        assert metrics.true_positives == 2
        assert metrics.false_positives == 1
        assert metrics.true_negatives == 1
        assert metrics.false_negatives == 1

        # Precision = TP / (TP + FP) = 2 / 3 = 0.6667
        assert 0.66 <= metrics.precision <= 0.67

        # Recall = TP / (TP + FN) = 2 / 3 = 0.6667
        assert 0.66 <= metrics.recall <= 0.67

    def test_get_validation_report(self, analyzer):
        """Test validation report generation"""
        analyzer.samples = [
            ValidationSample(
                commit_sha="c1",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["caching"],
                detection_method="keyword",
                true_label=True,
                validation_status="validated",
            ),
            ValidationSample(
                commit_sha="c2",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=[],
                detection_method="keyword",
                true_label=None,
                validation_status="pending",
            ),
        ]

        report = analyzer.get_validation_report()

        assert "sampling" in report
        assert "metrics" in report
        assert "error_analysis" in report
        assert "pattern_accuracy" in report

        assert report["sampling"]["total_samples"] == 2
        assert report["sampling"]["validated_samples"] == 1
        assert report["sampling"]["pending_samples"] == 1

    def test_inter_rater_reliability(self, analyzer):
        """Test Cohen's Kappa calculation"""
        # Create two sets of validations
        reviewer_a = [
            ValidationSample(
                commit_sha="c1",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["caching"],
                detection_method="keyword",
                true_label=True,
            ),
            ValidationSample(
                commit_sha="c2",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["async"],
                detection_method="keyword",
                true_label=True,
            ),
            ValidationSample(
                commit_sha="c3",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=[],
                detection_method="keyword",
                true_label=False,
            ),
        ]

        reviewer_b = [
            ValidationSample(
                commit_sha="c1",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["caching"],
                detection_method="keyword",
                true_label=True,  # Agreement
            ),
            ValidationSample(
                commit_sha="c2",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["async"],
                detection_method="keyword",
                true_label=False,  # Disagreement
            ),
            ValidationSample(
                commit_sha="c3",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=[],
                detection_method="keyword",
                true_label=False,  # Agreement
            ),
        ]

        reliability = analyzer.get_inter_rater_reliability(reviewer_a, reviewer_b)

        assert "cohens_kappa" in reliability
        assert "observed_agreement" in reliability
        assert "expected_agreement" in reliability
        assert "interpretation" in reliability

        # 2/3 agreement = 0.6667
        assert 0.66 <= reliability["observed_agreement"] <= 0.67

    def test_pattern_accuracy_analysis(self, analyzer):
        """Test per-pattern accuracy analysis"""
        analyzer.samples = [
            ValidationSample(
                commit_sha="c1",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["caching"],
                detection_method="keyword",
                true_label=True,
            ),
            ValidationSample(
                commit_sha="c2",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["caching"],
                detection_method="keyword",
                true_label=False,  # FP
            ),
            ValidationSample(
                commit_sha="c3",
                commit_message="",
                code_diff=None,
                repository="",
                detected_patterns=["async"],
                detection_method="keyword",
                true_label=True,
            ),
        ]

        pattern_accuracy = analyzer._analyze_pattern_accuracy()

        assert "caching" in pattern_accuracy
        assert "async" in pattern_accuracy

        # Caching: 1 TP, 1 FP → precision = 0.5
        assert pattern_accuracy["caching"]["true_positives"] == 1
        assert pattern_accuracy["caching"]["false_positives"] == 1
        assert pattern_accuracy["caching"]["precision"] == 0.5

        # Async: 1 TP, 0 FP → precision = 1.0
        assert pattern_accuracy["async"]["precision"] == 1.0
