import time
import pytest


class TestModuleImports:

    def test_import_greenmining(self):
        start = time.perf_counter()
        import greenmining

        elapsed = time.perf_counter() - start
        assert elapsed < 5.0, f"Import took {elapsed:.2f}s"
        assert hasattr(greenmining, "fetch_repositories")

    def test_import_config(self):
        from greenmining import config

        assert hasattr(config, "Config")
        assert hasattr(config, "get_config")
        assert hasattr(config, "_load_yaml_config")

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
        from greenmining.models import Repository, Commit, AnalysisResult, AggregatedStats

        assert Repository is not None
        assert Commit is not None
        assert AnalysisResult is not None
        assert AggregatedStats is not None

    def test_import_services(self):
        from greenmining.services import (
            GitHubGraphQLFetcher,
            CommitExtractor,
            DataAnalyzer,
            DataAggregator,
            ReportGenerator,
            LocalRepoAnalyzer,
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
            QualitativeAnalyzer,
            StatisticalAnalyzer,
            TemporalAnalyzer,
        )

        assert CodeDiffAnalyzer is not None
        assert QualitativeAnalyzer is not None
        assert StatisticalAnalyzer is not None
        assert TemporalAnalyzer is not None

    def test_import_energy(self):
        from greenmining.energy import EnergyMeter, RAPLEnergyMeter, CodeCarbonMeter
        from greenmining.energy.base import EnergyMetrics, EnergyBackend

        assert EnergyMeter is not None
        assert RAPLEnergyMeter is not None
        assert CodeCarbonMeter is not None
        assert EnergyMetrics is not None
        assert EnergyBackend is not None

    def test_import_presenters(self):
        from greenmining.presenters import ConsolePresenter

        assert ConsolePresenter is not None

    def test_import_controllers(self):
        from greenmining.controllers import RepositoryController

        assert RepositoryController is not None
