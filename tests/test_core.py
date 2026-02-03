import tempfile
import time
from pathlib import Path

import pytest


class TestModuleImports:
    def test_import_greenmining(self):
        start = time.perf_counter()
        import greenmining

        elapsed = time.perf_counter() - start
        assert elapsed < 5.0, f"Import took {elapsed:.2f}s"
        assert hasattr(greenmining, "fetch_repositories")

    def test_import_utils(self):
        from greenmining import utils

        assert hasattr(utils, "format_timestamp")
        assert hasattr(utils, "load_json_file")
        assert hasattr(utils, "save_json_file")
        assert hasattr(utils, "retry_on_exception")

    def test_import_gsf_patterns(self):
        from greenmining import gsf_patterns

        assert hasattr(gsf_patterns, "get_pattern_by_keywords")
        assert hasattr(gsf_patterns, "is_green_aware")

    def test_import_models(self):
        from greenmining.models import AggregatedStats, AnalysisResult, Commit, Repository

        assert Repository is not None
        assert Commit is not None
        assert AnalysisResult is not None
        assert AggregatedStats is not None

    def test_import_services(self):
        from greenmining.services import (
            CommitExtractor,
            DataAggregator,
            DataAnalyzer,
            GitHubGraphQLFetcher,
            LocalRepoAnalyzer,
            ReportGenerator,
        )

        assert GitHubGraphQLFetcher is not None
        assert CommitExtractor is not None
        assert DataAnalyzer is not None
        assert DataAggregator is not None
        assert ReportGenerator is not None
        assert LocalRepoAnalyzer is not None

    def test_import_analyzers(self):
        from greenmining.analyzers import (
            CodeDiffAnalyzer,
            StatisticalAnalyzer,
            TemporalAnalyzer,
        )

        assert CodeDiffAnalyzer is not None
        assert StatisticalAnalyzer is not None
        assert TemporalAnalyzer is not None

    def test_import_energy(self):
        from greenmining.energy import CodeCarbonMeter, EnergyMeter, RAPLEnergyMeter
        from greenmining.energy.base import EnergyBackend, EnergyMetrics

        assert EnergyMeter is not None
        assert RAPLEnergyMeter is not None
        assert CodeCarbonMeter is not None
        assert EnergyMetrics is not None
        assert EnergyBackend is not None

    def test_import_controllers(self):
        from greenmining.controllers import RepositoryController

        assert RepositoryController is not None


class TestModels:
    def test_repository_model(self):
        from greenmining.models import Repository

        repo = Repository(
            repo_id=123,
            name="test-repo",
            owner="test-owner",
            full_name="test-owner/test-repo",
            url="https://github.com/test-owner/test-repo",
            clone_url="https://github.com/test-owner/test-repo.git",
            language="Python",
            stars=100,
            forks=10,
            watchers=50,
            open_issues=5,
            last_updated="2025-01-15T10:00:00",
            created_at="2024-01-01T00:00:00",
            description="A test repository",
            main_branch="main",
        )
        assert repo.name == "test-repo"
        d = repo.to_dict()
        assert d["stars"] == 100

    def test_commit_model(self):
        from greenmining.models import Commit

        commit = Commit(
            commit_id="abc123",
            repo_name="test-repo",
            date="2025-01-15T10:00:00",
            author="test-author",
            author_email="test@example.com",
            message="Test commit message",
        )
        assert commit.commit_id == "abc123"
        d = commit.to_dict()
        assert d["message"] == "Test commit message"

    def test_analysis_result_model(self):
        from greenmining.models import AnalysisResult

        result = AnalysisResult(
            commit_id="abc123",
            repo_name="test-repo",
            date="2025-01-15T10:00:00",
            commit_message="optimize energy",
            green_aware=True,
        )
        assert result.green_aware is True
        d = result.to_dict()
        assert d["commit_id"] == "abc123"

    def test_aggregated_stats_model(self):
        from greenmining.models import AggregatedStats

        stats = AggregatedStats(
            summary={"total": 100},
            known_patterns={"cache": 10},
        )
        d = stats.to_dict()
        assert d["summary"]["total"] == 100


class TestEnergy:
    def test_energy_backend_enum(self):
        from greenmining.energy.base import EnergyBackend

        assert EnergyBackend.RAPL.value == "rapl"
        assert EnergyBackend.CODECARBON.value == "codecarbon"

    def test_energy_metrics_creation(self):
        from greenmining.energy.base import EnergyMetrics

        metrics = EnergyMetrics(
            joules=100.0,
            watts_avg=10.0,
            duration_seconds=10.0,
            cpu_energy_joules=80.0,
            dram_energy_joules=20.0,
        )
        assert metrics.joules == 100.0
        d = metrics.to_dict()
        assert d["watts_avg"] == 10.0

    def test_rapl_meter_init(self):
        from greenmining.energy import RAPLEnergyMeter

        meter = RAPLEnergyMeter()
        assert meter is not None
        assert isinstance(meter.is_available(), bool)

    def test_rapl_get_domains(self):
        from greenmining.energy import RAPLEnergyMeter

        meter = RAPLEnergyMeter()
        domains = meter.get_available_domains()
        assert isinstance(domains, list)

    @pytest.mark.skipif(
        not __import__("greenmining.energy", fromlist=["RAPLEnergyMeter"])
        .RAPLEnergyMeter()
        .is_available(),
        reason="RAPL not available",
    )
    def test_rapl_measure(self):
        from greenmining.energy import RAPLEnergyMeter

        meter = RAPLEnergyMeter()
        meter.start()
        time.sleep(0.1)
        metrics = meter.stop()
        assert metrics is not None
        assert metrics.duration_seconds >= 0.09

    def test_codecarbon_meter_init(self):
        from greenmining.energy import CodeCarbonMeter

        meter = CodeCarbonMeter()
        assert meter is not None
        assert isinstance(meter.is_available(), bool)


class TestGSFPatterns:
    def test_is_green_aware_positive(self):
        from greenmining.gsf_patterns import is_green_aware

        result = is_green_aware("optimize energy consumption and reduce battery drain")
        assert isinstance(result, bool)

    def test_is_green_aware_negative(self):
        from greenmining.gsf_patterns import is_green_aware

        result = is_green_aware("fixed typo in readme")
        assert isinstance(result, bool)

    def test_is_green_aware_empty(self):
        from greenmining.gsf_patterns import is_green_aware

        result = is_green_aware("")
        assert result is False

    def test_get_pattern_by_keywords_string(self):
        from greenmining.gsf_patterns import get_pattern_by_keywords

        result = get_pattern_by_keywords("optimize battery cache memory")
        assert result is None or isinstance(result, (dict, list))


class TestUtils:
    def test_format_timestamp(self):
        from datetime import datetime

        from greenmining import utils

        dt = datetime(2025, 1, 15, 10, 30, 0)
        result = utils.format_timestamp(dt)
        assert isinstance(result, str)
        assert "2025" in result

    def test_format_number(self):
        from greenmining import utils

        assert utils.format_number(1000) == "1,000"

    def test_format_percentage(self):
        from greenmining import utils

        result = utils.format_percentage(0.5)
        assert isinstance(result, str)

    def test_retry_decorator_success(self):
        from greenmining import utils

        @utils.retry_on_exception(max_retries=2, delay=0.01)
        def always_succeeds():
            return 42

        assert always_succeeds() == 42

    def test_colored_print(self, capsys):
        from greenmining import utils

        utils.colored_print("Test message", color="green")
        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_load_save_json(self):
        from greenmining import utils

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.json"
            data = {"key": "value", "num": 42}
            utils.save_json_file(data, path)
            loaded = utils.load_json_file(path)
            assert loaded == data


class TestServices:
    def test_commit_extractor_init(self):
        from greenmining.services import CommitExtractor

        extractor = CommitExtractor()
        assert extractor is not None

    def test_data_analyzer_init(self):
        from greenmining.services import DataAnalyzer

        analyzer = DataAnalyzer()
        assert analyzer is not None

    def test_data_aggregator_init(self):
        from greenmining.services import DataAggregator

        aggregator = DataAggregator()
        assert aggregator is not None

    def test_report_generator_init(self):
        from greenmining.services import ReportGenerator

        generator = ReportGenerator()
        assert generator is not None
        header = generator._generate_header()
        assert isinstance(header, str)

    def test_local_repo_analyzer_init(self):
        from greenmining.services import LocalRepoAnalyzer

        analyzer = LocalRepoAnalyzer()
        assert analyzer is not None

    def test_local_repo_analyzer_parse_url(self):
        from greenmining.services import LocalRepoAnalyzer

        analyzer = LocalRepoAnalyzer()
        owner, repo = analyzer._parse_repo_url("https://github.com/owner/repo.git")
        assert owner == "owner"
        assert repo == "repo"


class TestAnalyzers:
    def test_code_diff_analyzer_init(self):
        from greenmining.analyzers import CodeDiffAnalyzer

        analyzer = CodeDiffAnalyzer()
        assert analyzer is not None

    def test_statistical_analyzer_init(self):
        from greenmining.analyzers import StatisticalAnalyzer

        analyzer = StatisticalAnalyzer()
        assert analyzer is not None

    def test_statistical_effect_size(self):
        from greenmining.analyzers import StatisticalAnalyzer

        analyzer = StatisticalAnalyzer()
        result = analyzer.effect_size_analysis([1, 2, 3, 4, 5], [6, 7, 8, 9, 10])
        assert isinstance(result, dict)

    def test_temporal_analyzer_init(self):
        from greenmining.analyzers import TemporalAnalyzer

        analyzer = TemporalAnalyzer()
        assert analyzer is not None
