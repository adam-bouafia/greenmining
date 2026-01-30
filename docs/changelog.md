# Changelog

All notable changes to GreenMining are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.1.3] - 2026-01-30

### Fixed
- GraphQL `_parse_repository` now maps correctly to Repository dataclass fields (fixes `languages` keyword error)
- Removed all emojis from library output
- Removed marketing comments from codebase
- GraphQL search skips language filter when >5 languages to avoid query complexity limits
- Cleaned up deadcode blocks in repository_controller.py and github_fetcher.py

---

## [1.0.8] - 2026-01-30

### Enhanced Repository Support (Phase 1)

- **Batch URL Analysis API**: Analyze multiple repositories with configurable parallel workers
  - `analyze_repositories(urls, parallel_workers=4)` top-level function
  - `LocalRepoAnalyzer.analyze_repositories(urls, parallel_workers)` method
  - Thread pool-based parallelism for concurrent repository processing
- **Private Repository Support**: Authenticate with SSH keys or GitHub tokens
  - `LocalRepoAnalyzer(ssh_key_path="~/.ssh/id_rsa")` for SSH auth
  - `LocalRepoAnalyzer(github_token="ghp_xxx")` for HTTPS private repo access
  - Transparent URL token injection for private repository cloning

### Extended Energy Measurement (Phase 2)

- **CPU Energy Meter Backend**: Cross-platform energy estimation
  - Utilization-based power modeling using CPU TDP
  - Auto-detects platform (Linux, macOS, Windows)
  - Supports psutil for accurate CPU utilization tracking
  - `get_energy_meter("auto")` selects optimal backend
- **Integrated Energy Tracking**: Automatic energy measurement during analysis
  - `LocalRepoAnalyzer(energy_tracking=True, energy_backend="rapl")`
  - Energy metrics included in `RepositoryAnalysis.energy_metrics`
- **Carbon Footprint Reporting**: CO2 emissions calculation from energy data
  - `CarbonReporter` with 20+ country carbon intensity profiles
  - Cloud provider region support (AWS, GCP, Azure)
  - Equivalence calculations (tree-months, smartphone charges, km driven)

### Full Process Metrics Integration (Phase 3)

- **Complete Process Metrics**: All 8 process metrics (ChangeSet, CodeChurn, CommitsCount, ContributorsCount, ContributorsExperience, HistoryComplexity, HunksCount, LinesCount)
- **Method-Level Analysis**: Per-method metrics via Lizard integration
  - `LocalRepoAnalyzer(method_level_analysis=True)`
  - Extracts name, complexity, NLOC, token count, parameters per method
- **Source Code Access**: Before/after source code for refactoring detection
  - `LocalRepoAnalyzer(include_source_code=True)`
  - Full diff, change type, added/deleted lines per file

### Green MSR Techniques (Phase 4)

- **Power Regression Detection**: Identify commits that increased power consumption
  - `PowerRegressionDetector` with configurable threshold and test commands
  - Automated bisect-style regression detection across commit ranges
- **Metrics-to-Power Correlation**: Correlate code metrics with power consumption
  - `MetricsPowerCorrelator` with Pearson and Spearman correlation analysis
  - Feature importance scoring and significance testing
- **Version-by-Version Power Analysis**: Compare power across software versions
  - `VersionPowerAnalyzer` with multi-iteration measurement and warmup
  - Trend detection (increasing/decreasing/stable) with statistical reporting

### Web Dashboard (Phase 5)

- **Flask-based Dashboard**: Interactive visualization of analysis results
  - Repository listing, summary statistics, green rate metrics
  - REST API endpoints for programmatic access
  - `pip install greenmining[dashboard]` for dashboard support

### Dependencies

- Added optional `psutil` for cross-platform CPU energy measurement
- Added optional `flask` for web dashboard
- Added optional `codecarbon` for carbon tracking

---

## [1.0.4] - 2026-01-29

### 🚀 Major Performance Improvements

#### Changed
- **GraphQL API Migration** (5-10x faster repository fetching)
  - Replaced REST API with GitHub GraphQL API v4
  - Fetch 100 repos in 15 seconds (vs 2 minutes with REST)
  - Single request for repos + commits (vs 100+ REST calls)
  - Better rate limit efficiency: 5000 points/hour vs 5000 requests/hour
  - New `GitHubGraphQLFetcher` class replaces `GitHubFetcher`
  - Old REST implementation deadcoded for reference

- **Enhanced Code Pattern Detection** (13+ pattern types)
  - Expanded from 5 to 15 code-level detection patterns
  - **NEW patterns**: Serverless computing, CDN/edge, Compression, ML optimization,
    HTTP/2, gRPC, Container optimization, Green cloud regions, Auto-scaling,
    Code splitting, Green ML training
  - More accurate detection in code diffs

#### Removed
- **CLI Interface** - Library is now Python API-only
  - Removed `cli.py` and `main.py`
  - Removed CLI entry points
  - Use Python API instead (simpler for researchers and developers)

### Performance Metrics

| Metric | Before (REST) | After (GraphQL) | Improvement |
|--------|--------------|-----------------|-------------|
| Fetch 100 repos | 2 minutes | 15 seconds | **8x faster** |
| API requests | 100+ | 1-2 | **50x fewer** |
| Rate limit cost | ~100 requests | ~2 points | **50x better** |
| Pattern detection | 5 types | 15 types | **3x more** |

### Migration from 1.0.3

**No code changes needed!** The GraphQL migration is transparent:

```python
# This still works exactly the same - just 10x faster now!
from greenmining import fetch_repositories

repos = fetch_repositories(
    github_token="token",
    max_repos=100
)
# Now uses GraphQL internally (10x faster)
```

**If you were using CLI:**
- CLI has been removed
- Use the Python API instead
- See updated documentation for API examples

**New features available:**
```python
# Use GraphQL directly for more control
from greenmining.services.github_graphql_fetcher import GitHubGraphQLFetcher

fetcher = GitHubGraphQLFetcher(token="token")
repos = fetcher.search_repositories(keywords="kubernetes", max_repos=100)
```

---

## [0.2.0] - 2024-XX-XX

### Added
- **URL-based Analysis**: Analyze repositories directly by URL with full commit extraction
  - `greenmining analyze <url>` command (unified single/batch support)
  - `LocalRepoAnalyzer` service for Python API
- **Energy Measurement**: Track energy consumption during analysis
  - RAPL backend for Linux (Intel CPUs)
  - CodeCarbon backend for cross-platform carbon tracking
  - `--energy` and `--energy-backend` CLI options
- **Commit Extraction**: Rich commit metrics and process metrics
  - Delta Maintainability Model (DMM) metrics
  - Process metrics (code churn, change set, contributor count)
  - Structural metrics (complexity, lines of code)

### Changed
- Renamed "Enhanced" terminology to standard naming throughout codebase
- Simplified analyzer architecture
- Consolidated CLI: unified `analyze` command handles both local data and URL analysis
  - Previous: `analyze`, `analyze-url`, `analyze-urls` (3 separate commands)
  - Now: `analyze [SOURCES...]` - auto-detects URLs vs local mode

### Removed
- NLP-based semantic analysis (simplified to keyword matching)
- ML-based classification (not needed for pattern detection)
- External ML model dependencies

### Fixed
- Pattern detection accuracy improvements
- Configuration loading from .env files
- Report generation formatting

---

## [0.1.0] - 2024-XX-XX

### Added
- Initial release
- GSF pattern detection (122 patterns, 15 categories)
- GitHub repository fetching
- Commit extraction and analysis
- Statistical analysis with effect sizes
- Temporal trend analysis
- Docker support
- Configuration via environment variables

### Dependencies
- Python 3.9+
- Built-in repository mining and commit extraction
- python-dotenv for configuration

---

## Migration Guide

### From 0.1.x to 1.0.x

#### API Changes

1. **Import paths unchanged**:
   ```python
   # Still works
   from greenmining import is_green_aware, GSF_PATTERNS
   ```

2. **New services**:
   ```python
   # New in 0.2.0+
   from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer
   from greenmining.energy.base import EnergyMeasurer
   ```

3. **Removed NLP/ML features**:
   ```python
   # These no longer exist - remove from your code
   # from greenmining.analyzers import SemanticAnalyzer  # Removed
   # from greenmining.analyzers import MLClassifier  # Removed
   ```

#### From 1.0.3 to 1.0.4 (CLI Removal)

**CLI has been removed in 1.0.4.** Use the Python API:

```python
# Old CLI: greenmining analyze https://github.com/org/repo
# New Python API:
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer()
result = analyzer.analyze_repository("https://github.com/org/repo")
```

---

## Links

- [GitHub Repository](https://github.com/adam-bouafia/greenmining)
- [Documentation](https://greenmining.readthedocs.io)
- [PyPI Package](https://pypi.org/project/greenmining/)
