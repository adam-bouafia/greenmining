# GreenMining Library Reference

## Description

GreenMining is an empirical Python library for Mining Software Repositories (MSR) in Green IT research. It analyzes GitHub repositories to detect green software engineering practices by matching commit messages and code changes against the Green Software Foundation (GSF) pattern catalog. The library supports energy measurement during analysis using Intel RAPL, CodeCarbon, or CPU utilization-based estimation, and provides statistical, temporal, and qualitative analysis capabilities.

**Version:** 1.1.9
**License:** MIT
**PyPI:** [greenmining](https://pypi.org/project/greenmining/)
**Documentation:** [greenmining.readthedocs.io](https://greenmining.readthedocs.io)

---

## File Tree

```
greenmining/
    __init__.py
    __main__.py
    __version__.py
    config.py
    gsf_patterns.py
    utils.py
    models/
        __init__.py
        repository.py
        commit.py
        analysis_result.py
        aggregated_stats.py
    services/
        __init__.py
        github_fetcher.py          (deprecated)
        github_graphql_fetcher.py
        commit_extractor.py
        data_analyzer.py
        data_aggregator.py
        local_repo_analyzer.py
        reports.py
    analyzers/
        __init__.py
        statistical_analyzer.py
        temporal_analyzer.py
        qualitative_analyzer.py
        code_diff_analyzer.py
        metrics_power_correlator.py
        power_regression.py
        version_power_analyzer.py
    energy/
        __init__.py
        base.py
        rapl.py
        cpu_meter.py
        codecarbon_meter.py
        carbon_reporter.py
    controllers/
        __init__.py
        repository_controller.py
    presenters/
        __init__.py
        console_presenter.py
```

---

## Module Reference

### `greenmining/__init__.py`

Top-level package entry point. Exposes the two main high-level API functions and the GSF pattern utilities.

| Function | Parameters | Description |
|----------|-----------|-------------|
| `fetch_repositories()` | `github_token`, `max_repos`, `min_stars`, `languages`, `keywords`, `created_after`, `created_before`, `pushed_after`, `pushed_before` | Search GitHub for repositories using GraphQL API v4. Returns a list of `Repository` objects matching the given filters. |
| `analyze_repositories()` | `urls`, `max_commits`, `parallel_workers`, `output_format`, `energy_tracking`, `energy_backend`, `method_level_analysis`, `include_source_code`, `ssh_key_path`, `github_token`, `since_date`, `to_date` | Clone and analyze multiple repositories from URLs using PyDriller. Supports energy measurement, method-level Lizard metrics, and source code extraction. Returns a list of `RepositoryAnalysis` objects. |

**Exports:** `Config`, `GSF_PATTERNS`, `GREEN_KEYWORDS`, `is_green_aware`, `get_pattern_by_keywords`, `fetch_repositories`, `analyze_repositories`, `__version__`

---

### `greenmining/__main__.py`

Allows running as `python -m greenmining`. Prints version and usage information.

---

### `greenmining/config.py`

Configuration management supporting `.env` files, environment variables, and YAML configuration (`greenmining.yaml`).

#### `_load_yaml_config(yaml_path)`

Loads YAML configuration from file. Returns empty dict if the file does not exist or PyYAML is not installed.

#### class `Config`

| Attribute | Default | Source | Description |
|-----------|---------|--------|-------------|
| `GITHUB_TOKEN` | required | env | GitHub personal access token |
| `GITHUB_SEARCH_KEYWORDS` | `["microservices", ...]` | YAML/env | Search keywords for repository discovery |
| `SUPPORTED_LANGUAGES` | `["Java", "Python", "Go", ...]` | YAML/env | Languages to filter |
| `MAX_REPOS` | `100` | env | Maximum repositories to fetch |
| `COMMITS_PER_REPO` | `50` | YAML/env | Maximum commits per repository |
| `DAYS_BACK` | `730` | YAML/env | Analysis time window in days |
| `SKIP_MERGES` | `True` | YAML | Skip merge commits |
| `MIN_STARS` | `100` | YAML/env | Minimum stars filter |
| `ENERGY_ENABLED` | `False` | YAML/env | Enable energy measurement |
| `ENERGY_BACKEND` | `"rapl"` | YAML/env | Energy backend selection |
| `CARBON_TRACKING` | `False` | YAML/env | Enable CO2 tracking |
| `COUNTRY_ISO` | `"USA"` | YAML/env | Country for carbon intensity |
| `OUTPUT_DIR` | `./data` | YAML/env | Output directory for results |

| Method | Description |
|--------|-------------|
| `__init__(env_file, yaml_file)` | Load configuration from environment and YAML. YAML values take precedence for supported options. |
| `validate()` | Validate that all required configuration attributes are present. |
| `_parse_repository_urls(urls_str)` | Parse comma-separated repository URLs from environment variable. |

#### `get_config(env_file)`

Singleton factory that returns or creates a global `Config` instance.

---

### `greenmining/gsf_patterns.py`

Contains the Green Software Foundation pattern catalog and keyword matching logic.

**`GSF_PATTERNS`** -- Dictionary of 124 green software patterns across 15 categories:

| Category | Count | Examples |
|----------|-------|---------|
| cloud | 35+ | Cache Static Data, Autoscaling, Serverless, Right-size Resources |
| web | 15+ | Lazy Loading, Minimize Data Transfer, Optimize Images |
| ai | 15+ | Model Quantization, Knowledge Distillation, Early Stopping |
| database | 5+ | Database Indexing, Query Optimization, Prepared Statements |
| networking/network | 8+ | Connection Pooling, gRPC Optimization, API Gateway |
| general | 8+ | Async Processing, Batch Processing, Memoization |
| resource | 2 | Resource Limits, Dynamic Resource Allocation |
| caching | 2 | Multi-Level Caching, Cache Invalidation Strategy |
| data | 3 | Data Deduplication, Efficient Serialization, Pagination |
| async | 3 | Event-Driven Architecture, Eliminate Polling, Reactive Streams |
| code | 4 | Algorithm Optimization, Code Efficiency, Garbage Collection Tuning |
| monitoring | 3 | Energy-Aware Monitoring, Performance Profiling, APM |
| microservices | 4 | Service Decomposition, Service Co-location, Graceful Shutdown |
| infrastructure | 4 | Minimal Container Images, Renewable Energy Regions, IaC |

Each pattern has: `name`, `category`, `keywords` (list), `description`, `sci_impact`.

**`GREEN_KEYWORDS`** -- List of 332 keywords used for green awareness detection (e.g., "energy", "cache", "optimize", "serverless", "quantization").

| Function | Parameters | Description |
|----------|-----------|-------------|
| `get_pattern_by_keywords(commit_message)` | `commit_message: str` | Match a commit message against all GSF patterns. Returns list of matched pattern names. |
| `is_green_aware(commit_message)` | `commit_message: str` | Check if a commit message contains any green software keyword. Returns boolean. |

---

### `greenmining/utils.py`

Utility functions for file I/O, formatting, retry logic, and console output.

| Function | Parameters | Description |
|----------|-----------|-------------|
| `format_timestamp(dt)` | `dt: Optional[datetime]` | Format datetime as ISO 8601 string. Defaults to `utcnow()`. |
| `load_json_file(path)` | `path: Path` | Load and parse a JSON file. |
| `save_json_file(data, path, indent)` | `data: dict, path: Path, indent: int` | Save data to JSON file, creating parent directories. |
| `load_csv_file(path)` | `path: Path` | Load CSV file as pandas DataFrame. |
| `save_csv_file(df, path)` | `df: DataFrame, path: Path` | Save DataFrame to CSV file. |
| `estimate_tokens(text)` | `text: str` | Estimate token count (len/4). |
| `estimate_cost(tokens, model)` | `tokens: int, model: str` | Estimate API cost based on Claude Sonnet 4 pricing. |
| `retry_on_exception(max_retries, delay, exponential_backoff, exceptions)` | decorator args | Decorator that retries a function on exception with configurable backoff. |
| `colored_print(text, color)` | `text: str, color: str` | Print colored text using colorama. Supported colors: red, green, yellow, blue, magenta, cyan, white. |
| `handle_github_rate_limit(response)` | `response` | Check for HTTP 403 and raise exception on rate limit. |
| `format_number(num)` | `num: int` | Format number with thousand separators. |
| `format_percentage(value, decimals)` | `value: float, decimals: int` | Format float as percentage string. |
| `format_duration(seconds)` | `seconds: float` | Format duration as human-readable string (e.g., "2m 30s"). |
| `truncate_text(text, max_length)` | `text: str, max_length: int` | Truncate text with "..." suffix. |
| `create_checkpoint(checkpoint_file, data)` | `checkpoint_file: Path, data: dict` | Save checkpoint JSON for resumable operations. |
| `load_checkpoint(checkpoint_file)` | `checkpoint_file: Path` | Load checkpoint data if file exists. |
| `print_banner(title)` | `title: str` | Print formatted banner with decorators. |
| `print_section(title)` | `title: str` | Print section header with separator line. |

---

## Models

### `greenmining/models/repository.py`

#### class `Repository` (dataclass)

Represents a GitHub repository with all metadata.

| Field | Type | Description |
|-------|------|-------------|
| `repo_id` | `int` | Sequential identifier |
| `name` | `str` | Repository name |
| `owner` | `str` | Repository owner/organization |
| `full_name` | `str` | `owner/name` format |
| `url` | `str` | HTML URL |
| `clone_url` | `str` | Git clone URL |
| `language` | `Optional[str]` | Primary programming language |
| `stars` | `int` | Star count |
| `forks` | `int` | Fork count |
| `watchers` | `int` | Watcher count |
| `open_issues` | `int` | Open issue count |
| `last_updated` | `str` | Last update ISO date |
| `created_at` | `str` | Creation ISO date |
| `description` | `Optional[str]` | Repository description |
| `main_branch` | `str` | Default branch name |
| `topics` | `list[str]` | Repository topics |
| `size` | `int` | Repository size in KB |
| `archived` | `bool` | Whether archived |
| `license` | `Optional[str]` | License key |

| Method | Description |
|--------|-------------|
| `to_dict()` | Convert to dictionary. |
| `from_dict(data)` | Class method: create from dictionary. |
| `from_github_repo(repo, repo_id)` | Class method: create from PyGithub repository object. |

---

### `greenmining/models/commit.py`

#### class `Commit` (dataclass)

Represents a Git commit with metadata.

| Field | Type | Description |
|-------|------|-------------|
| `commit_id` | `str` | Commit SHA hash |
| `repo_name` | `str` | Repository full name |
| `date` | `str` | Commit date ISO string |
| `author` | `str` | Author name |
| `author_email` | `str` | Author email |
| `message` | `str` | Commit message |
| `files_changed` | `list[str]` | Modified file paths |
| `lines_added` | `int` | Lines added |
| `lines_deleted` | `int` | Lines deleted |
| `insertions` | `int` | Insertions count |
| `deletions` | `int` | Deletions count |
| `is_merge` | `bool` | Whether this is a merge commit |
| `in_main_branch` | `bool` | Whether commit is in main branch |

| Method | Description |
|--------|-------------|
| `to_dict()` | Convert to dictionary. |
| `from_dict(data)` | Class method: create from dictionary. |
| `from_pydriller_commit(commit, repo_name)` | Class method: create from PyDriller commit object. |

---

### `greenmining/models/analysis_result.py`

#### class `AnalysisResult` (dataclass)

Represents the analysis result for a single commit.

| Field | Type | Description |
|-------|------|-------------|
| `commit_id` | `str` | Commit SHA |
| `repo_name` | `str` | Repository name |
| `date` | `str` | Commit date |
| `commit_message` | `str` | Full commit message |
| `green_aware` | `bool` | Whether commit is green-aware |
| `green_evidence` | `Optional[str]` | Evidence for green classification |
| `known_pattern` | `Optional[str]` | Matched GSF pattern name |
| `pattern_confidence` | `Optional[str]` | Confidence level (HIGH/MEDIUM/LOW) |
| `emergent_pattern` | `Optional[str]` | Novel pattern description |
| `files_changed` | `list` | Modified files |
| `lines_added` | `int` | Lines added |
| `lines_deleted` | `int` | Lines deleted |

---

### `greenmining/models/aggregated_stats.py`

#### class `AggregatedStats` (dataclass)

Holds aggregated analysis statistics.

| Field | Type | Description |
|-------|------|-------------|
| `summary` | `dict` | Overall summary statistics |
| `known_patterns` | `dict` | Pattern frequency data |
| `repositories` | `list[dict]` | Per-repository statistics |
| `languages` | `dict` | Per-language statistics |
| `timestamp` | `Optional[str]` | Aggregation timestamp |

---

## Services

### `greenmining/services/github_graphql_fetcher.py`

#### class `GitHubGraphQLFetcher`

Fetches repositories and commits from GitHub using GraphQL API v4. Handles pagination and rate limiting.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(token)` | `token: str` | Initialize with GitHub personal access token. |
| `search_repositories(keywords, max_repos, min_stars, languages, created_after, created_before, pushed_after, pushed_before)` | see params | Search for repositories matching criteria. Paginates automatically. Returns list of `Repository` objects. |
| `get_repository_commits(owner, name, max_commits)` | `owner: str, name: str, max_commits: int` | Fetch commit history for a specific repository. Returns list of commit dictionaries. |
| `save_results(repositories, output_file)` | `repositories: List[Repository], output_file: str` | Save repository list to JSON file. |
| `_build_search_query(...)` | internal | Build GitHub search query string with filters (stars, languages, dates). |
| `_execute_query(query, variables)` | internal | Execute a GraphQL query against GitHub API. |
| `_parse_repository(node, repo_id)` | internal | Parse GraphQL response node into `Repository` object. |

---

### `greenmining/services/github_fetcher.py`

**Deprecated.** Legacy REST API fetcher. Use `GitHubGraphQLFetcher` instead.

---

### `greenmining/services/commit_extractor.py`

#### class `CommitExtractor`

Extracts commit data from repositories using the GitHub REST API (PyGithub).

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(max_commits, skip_merges, days_back, github_token, timeout)` | see params | Initialize with extraction settings. Default: 50 commits, skip merges, 730 days back, 60s timeout. |
| `extract_from_repositories(repositories)` | `repositories: list` | Extract commits from a list of repositories. Handles timeouts and errors per repository. Uses SIGALRM for timeout enforcement. |
| `save_results(commits, output_file, repos_count)` | `commits: list, output_file: Path, repos_count: int` | Save extracted commits to JSON with metadata. |
| `_extract_repo_commits(repo)` | internal | Extract commits from a single repository via GitHub API. Decorated with `@retry_on_exception`. |
| `_extract_commit_metadata(commit, repo_name)` | internal | Extract metadata from a PyDriller commit object. |
| `_extract_commit_metadata_from_github(commit, repo_name)` | internal | Extract metadata from a PyGithub commit object. |

---

### `greenmining/services/data_analyzer.py`

#### class `DataAnalyzer`

Analyzes commits for green software patterns using GSF keywords and optional code diff analysis.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(batch_size, enable_diff_analysis)` | `batch_size: int, enable_diff_analysis: bool` | Initialize with GSF patterns. Optionally enables `CodeDiffAnalyzer` for deeper code inspection. |
| `analyze_commits(commits, resume_from)` | `commits: list, resume_from: int` | Analyze a list of commit dictionaries. Returns analysis results with green awareness, matched patterns, confidence, and metadata. |
| `save_results(results, output_file)` | `results: list, output_file: Path` | Save analysis results to JSON with summary statistics. |
| `_analyze_commit(commit)` | internal | Analyze a single commit: check green awareness via `is_green_aware()`, match GSF patterns via `get_pattern_by_keywords()`, calculate confidence, and optionally run diff analysis. |
| `_check_green_awareness(message, files)` | internal | Check commit message and file names for green keywords. |
| `_detect_known_pattern(message, files)` | internal | Detect known green software pattern from message and file names. |

---

### `greenmining/services/data_aggregator.py`

#### class `DataAggregator`

Aggregates analysis results and generates summary statistics. Optionally integrates statistical and temporal analysis.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(enable_stats, enable_temporal, temporal_granularity)` | `enable_stats: bool, enable_temporal: bool, temporal_granularity: str` | Initialize aggregator. When `enable_stats=True`, creates a `StatisticalAnalyzer`. When `enable_temporal=True`, creates a `TemporalAnalyzer`. |
| `aggregate(analysis_results, repositories)` | `analysis_results: list, repositories: list` | Compute summary, pattern analysis, per-repo stats, per-language stats. Optionally adds statistical analysis (trends, correlations, effect sizes) and temporal trend analysis. |
| `save_results(aggregated_data, json_file, csv_file, analysis_results)` | see params | Save aggregated data to JSON and detailed results to CSV. |
| `print_summary(aggregated_data)` | `aggregated_data: dict` | Print formatted summary tables to console using tabulate. |
| `_generate_summary(results, repos)` | internal | Calculate total commits, green count, percentage, repos with green commits. |
| `_analyze_known_patterns(results)` | internal | Count and rank detected GSF patterns with confidence breakdown. |
| `_analyze_emergent_patterns(results)` | internal | Collect novel patterns not in the GSF catalog. |
| `_generate_repo_stats(results, repos)` | internal | Compute per-repository green commit statistics. |
| `_generate_language_stats(results, repos)` | internal | Compute per-language green commit statistics. |
| `_generate_statistics(results)` | internal | Run temporal trends (Mann-Kendall), pattern correlations, effect sizes (Cohen's d), and descriptive statistics. |

---

### `greenmining/services/local_repo_analyzer.py`

The core analysis engine. Clones repositories from URLs and analyzes commits using PyDriller.

#### class `MethodMetrics` (dataclass)

Per-method analysis metrics extracted via Lizard integration through PyDriller.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Method name |
| `long_name` | `str` | Fully qualified method name |
| `filename` | `str` | Source file name |
| `nloc` | `int` | Lines of code |
| `complexity` | `int` | Cyclomatic complexity |
| `token_count` | `int` | Token count |
| `parameters` | `int` | Parameter count |
| `start_line` | `int` | Start line number |
| `end_line` | `int` | End line number |

#### class `SourceCodeChange` (dataclass)

Source code before/after a commit for refactoring detection.

| Field | Type | Description |
|-------|------|-------------|
| `filename` | `str` | File name |
| `source_code_before` | `Optional[str]` | Source code before the commit |
| `source_code_after` | `Optional[str]` | Source code after the commit |
| `diff` | `Optional[str]` | Unified diff |
| `added_lines` | `int` | Lines added |
| `deleted_lines` | `int` | Lines deleted |
| `change_type` | `str` | ADD, DELETE, MODIFY, or RENAME |

#### class `CommitAnalysis` (dataclass)

Full analysis result for a single commit, including GSF patterns, DMM metrics, structural metrics, method-level analysis, source code, and energy data.

| Field | Type | Description |
|-------|------|-------------|
| `hash` | `str` | Commit SHA |
| `message` | `str` | Commit message |
| `author` / `author_email` | `str` | Author info |
| `date` | `datetime` | Author date |
| `green_aware` | `bool` | Green awareness flag |
| `gsf_patterns_matched` | `List[str]` | Matched GSF pattern names |
| `pattern_count` | `int` | Number of patterns matched |
| `pattern_details` | `List[Dict]` | Full pattern info (name, category, description, sci_impact) |
| `confidence` | `str` | high / medium / low |
| `files_modified` | `List[str]` | Modified file names |
| `insertions` / `deletions` | `int` | Line change counts |
| `dmm_unit_size` | `Optional[float]` | Delta Maintainability Model: unit size |
| `dmm_unit_complexity` | `Optional[float]` | DMM: unit complexity |
| `dmm_unit_interfacing` | `Optional[float]` | DMM: unit interfacing |
| `total_nloc` | `int` | Total lines of code across modified files |
| `total_complexity` | `int` | Total cyclomatic complexity |
| `max_complexity` | `int` | Maximum complexity of any modified file |
| `methods_count` | `int` | Total methods across modified files |
| `methods` | `List[MethodMetrics]` | Per-method metrics (when `method_level_analysis=True`) |
| `source_changes` | `List[SourceCodeChange]` | Source code changes (when `include_source_code=True`) |
| `energy_joules` | `Optional[float]` | Energy consumed (when `energy_tracking=True`) |
| `energy_watts_avg` | `Optional[float]` | Average power draw |

#### class `RepositoryAnalysis` (dataclass)

Complete analysis result for a repository.

| Field | Type | Description |
|-------|------|-------------|
| `url` | `str` | Repository URL |
| `name` | `str` | Repository full name |
| `total_commits` | `int` | Total commits analyzed |
| `green_commits` | `int` | Green-aware commit count |
| `green_commit_rate` | `float` | Green commit percentage |
| `commits` | `List[CommitAnalysis]` | Per-commit analysis results |
| `process_metrics` | `Dict` | PyDriller process metrics |
| `energy_metrics` | `Optional[Dict]` | Energy measurement results |

#### class `LocalRepoAnalyzer`

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(clone_path, max_commits, days_back, skip_merges, compute_process_metrics, cleanup_after, ssh_key_path, github_token, energy_tracking, energy_backend, method_level_analysis, include_source_code, process_metrics, since_date, to_date)` | see params | Initialize analyzer with all analysis options. |
| `analyze_repository(url)` | `url: str` | Clone and analyze a single repository. Handles authentication (HTTPS token injection, SSH key). Creates a fresh energy meter per repository for thread safety. Returns `RepositoryAnalysis`. |
| `analyze_repositories(urls, parallel_workers, output_format)` | `urls: List[str], parallel_workers: int, output_format: str` | Analyze multiple repositories sequentially or in parallel using ThreadPoolExecutor. |
| `analyze_commit(commit)` | `commit` (PyDriller) | Analyze a single PyDriller commit object. Extracts green awareness, GSF patterns, DMM metrics, structural metrics, optional method-level and source code data. |
| `_compute_process_metrics(repo_path)` | internal | Compute 8 PyDriller process metrics: ChangeSet, CodeChurn, CommitsCount, ContributorsCount, ContributorsExperience, HistoryComplexity, HunksCount, LinesCount. |
| `_prepare_auth_url(url)` | internal | Inject GitHub token into HTTPS URL for private repository access. |
| `_setup_ssh_env()` | internal | Configure SSH environment for private repository cloning. |
| `_parse_repo_url(url)` | internal | Parse owner and name from HTTPS or SSH GitHub URLs. |
| `_extract_method_metrics(commit)` | internal | Extract per-method Lizard metrics from modified files. |
| `_extract_source_changes(commit)` | internal | Extract source code before/after for each modified file. |

---

### `greenmining/services/reports.py`

#### class `ReportGenerator`

Generates comprehensive Markdown reports from aggregated analysis data.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `generate_report(aggregated_data, analysis_data, repos_data)` | see params | Generate a full Markdown report with sections: Header, Executive Summary, Methodology, Results, Discussion, Limitations, Conclusion. |
| `save_report(report_content, output_file)` | `report_content: str, output_file: Path` | Write report to Markdown file. |
| `_generate_header()` | internal | Report title and metadata. |
| `_generate_executive_summary(data)` | internal | Key findings, percentage summaries, implications. |
| `_generate_methodology(repos_data, analysis_data)` | internal | Repository selection criteria, data extraction approach, analysis methodology (Q1/Q2/Q3). |
| `_generate_results(data)` | internal | Green awareness section, known patterns table, emergent patterns, per-repo analysis, statistics. |
| `_generate_discussion(data)` | internal | Interpretation, developer approaches, gap analysis, implications. |
| `_generate_limitations()` | internal | Sample bias, commit message limitations, scope limitations. |
| `_generate_conclusion(data)` | internal | Key findings, research question answers, recommendations. |

---

## Analyzers

### `greenmining/analyzers/statistical_analyzer.py`

#### class `StatisticalAnalyzer`

Advanced statistical analysis using scipy and numpy.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `analyze_pattern_correlations(commit_data)` | `commit_data: DataFrame` | Compute Pearson correlation matrix between pattern columns. Identifies significant pairs (|r| > 0.5). |
| `temporal_trend_analysis(commits_df)` | `commits_df: DataFrame` | Monthly aggregation, Mann-Kendall trend test, optional seasonal decomposition (requires 24+ months), change point detection via rolling variance. Handles timezone-aware datetimes. |
| `effect_size_analysis(group1, group2)` | `group1: List[float], group2: List[float]` | Cohen's d effect size with magnitude classification (negligible/small/medium/large). Includes independent t-test for significance. |
| `pattern_adoption_rate_analysis(commits_df)` | `commits_df: DataFrame` | Analyze time-to-first-adoption, monthly adoption frequency, and pattern stickiness per pattern. |

---

### `greenmining/analyzers/temporal_analyzer.py`

#### class `TemporalMetrics` (dataclass)

Metrics for a specific time period: commit count, green count, green rate, unique patterns, dominant pattern, velocity.

#### class `TrendAnalysis` (dataclass)

Trend analysis results: direction (increasing/decreasing/stable), slope, R-squared, start/end rates, change percentage.

#### class `TemporalAnalyzer`

Analyze temporal patterns in green software adoption over configurable time granularities.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(granularity)` | `granularity: str` | Initialize with time granularity: "day", "week", "month", "quarter", or "year". |
| `group_commits_by_period(commits, date_field)` | `commits: List[Dict], date_field: str` | Group commits into time periods based on granularity. Handles both datetime objects and ISO strings. |
| `calculate_period_metrics(period_key, commits, analysis_results)` | see params | Calculate `TemporalMetrics` for a single period. |
| `analyze_trends(commits, analysis_results)` | `commits: List[Dict], analysis_results: List[Dict]` | Full temporal analysis: period metrics, linear trend (least squares), cumulative adoption curve, velocity trend, and pattern evolution timeline. |

---

### `greenmining/analyzers/qualitative_analyzer.py`

#### class `ValidationSample` (dataclass)

Represents a single validation sample with commit data, detected patterns, and manual review fields.

#### class `ValidationMetrics` (dataclass)

Precision, recall, F1 score, and accuracy metrics.

#### class `QualitativeAnalyzer`

Framework for manual validation and inter-rater reliability assessment.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(sample_size, stratify_by)` | `sample_size: int, stratify_by: str` | Initialize with sample size (default 30) and stratification method ("pattern" or "repository"). |
| `generate_validation_samples(commits, analysis_results, include_negatives)` | see params | Generate stratified validation samples. 80% positive / 20% negative split for false-negative detection. |
| `export_samples_for_review(output_path)` | `output_path: str` | Export samples to JSON for manual review. Includes instructions for reviewers. |
| `import_validated_samples(input_path)` | `input_path: str` | Import manually validated samples from JSON. Updates sample statuses. |
| `calculate_metrics()` | none | Calculate precision, recall, F1, and accuracy from validated samples. |
| `get_validation_report()` | none | Generate comprehensive report: sampling info, metrics, error analysis (false positives/negatives), per-pattern accuracy. |
| `get_inter_rater_reliability(samples_a, samples_b)` | two lists of `ValidationSample` | Calculate Cohen's Kappa for inter-rater reliability with interpretation (slight/fair/moderate/substantial/almost perfect). |

---

### `greenmining/analyzers/code_diff_analyzer.py`

#### class `CodeDiffAnalyzer`

Analyze code diffs to detect green software patterns in actual code changes. Contains regex-based pattern signatures for 13 categories:

- **caching** -- imports, annotations (`@cache`, `@lru_cache`), function calls, variable names
- **resource_optimization** -- Kubernetes resource limits, Docker optimization
- **database_optimization** -- indexes, query optimization, connection pooling
- **async_processing** -- async/await, ThreadPoolExecutor, Celery
- **lazy_loading** -- lazy, defer, dynamic import
- **serverless_computing** -- AWS Lambda, Azure Functions, serverless frameworks
- **cdn_edge** -- CloudFront, Cloudflare, edge caching
- **compression** -- gzip, brotli, zstd, lz4
- **model_optimization** -- quantization, pruning, ONNX, TensorRT
- **efficient_protocols** -- HTTP/2, gRPC, protobuf
- **container_optimization** -- Alpine, distroless, multi-stage builds
- **green_regions** -- renewable energy regions
- **auto_scaling** -- HPA, KEDA, scale-to-zero
- **code_splitting** -- React.lazy, Suspense, dynamic import
- **green_ml_training** -- early stopping, mixed precision, gradient checkpointing

| Method | Parameters | Description |
|--------|-----------|-------------|
| `analyze_commit_diff(commit)` | `commit: Commit` (PyDriller) | Analyze all modified files in a commit. Returns patterns detected, evidence (file:line), confidence score, and code metrics. |
| `_detect_patterns_in_line(code_line)` | internal | Match a single line against all pattern signatures. |
| `_calculate_metrics(commit)` | internal | Calculate lines added/removed, files changed, net lines, complexity change. |
| `_calculate_diff_confidence(patterns, evidence, metrics)` | internal | Confidence scoring: high (3+ patterns, 5+ evidence), medium (2+ patterns, 3+ evidence), low. |
| `_is_code_file(modified_file)` | internal | Check if file is code (.py, .java, .go, etc.) or Kubernetes manifest. |

---

### `greenmining/analyzers/metrics_power_correlator.py`

#### class `CorrelationResult` (dataclass)

Result of a metrics-to-power correlation: Pearson r/p, Spearman r/p, significance, strength classification.

#### class `MetricsPowerCorrelator`

Correlate code metrics (complexity, NLOC, churn) with power consumption measurements.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(significance_level)` | `significance_level: float` | Initialize with p-value threshold (default 0.05). |
| `fit(metrics, metrics_values, power_measurements)` | `metrics: List[str], metrics_values: Dict, power_measurements: List[float]` | Compute Pearson and Spearman correlations for each metric against power data. Requires at least 3 data points. Computes feature importance (normalized absolute Spearman). |
| `pearson` (property) | none | Get Pearson correlation values for all metrics. |
| `spearman` (property) | none | Get Spearman correlation values for all metrics. |
| `feature_importance` (property) | none | Get normalized feature importance scores. |
| `get_results()` | none | Get all `CorrelationResult` objects. |
| `get_significant_correlations()` | none | Filter to only statistically significant results. |
| `summary()` | none | Generate summary with counts, correlations, feature importance, strongest positive/negative. |

---

### `greenmining/analyzers/power_regression.py`

#### class `PowerRegression` (dataclass)

A detected power regression: commit SHA, message, author, date, power before/after (watts), energy before/after (joules), percentage increase.

#### class `PowerRegressionDetector`

Detect commits that caused power consumption regressions by running a test command at each commit.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(test_command, energy_backend, threshold_percent, iterations, warmup_iterations)` | see params | Initialize detector. Default: `pytest tests/ -x`, RAPL backend, 5% threshold, 5 iterations, 1 warmup. |
| `detect(repo_path, baseline_commit, target_commit, max_commits)` | see params | Iterate through commits from baseline to target. At each commit: checkout, run test command, measure energy. Flag commits where energy increased above threshold. Returns list of `PowerRegression` objects. |

---

### `greenmining/analyzers/version_power_analyzer.py`

#### class `VersionPowerProfile` (dataclass)

Power profile for a single version: version tag, commit SHA, energy (joules), power (watts avg), duration, iterations, energy standard deviation.

#### class `VersionPowerReport` (dataclass)

Complete power analysis report across versions: list of profiles, trend direction, total change %, most/least efficient versions.

| Method | Description |
|--------|-------------|
| `to_dict()` | Convert to dictionary. |
| `summary()` | Generate human-readable summary string. |

#### class `VersionPowerAnalyzer`

Measure and compare power consumption across software versions/tags.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(test_command, energy_backend, iterations, warmup_iterations)` | see params | Initialize with test command and measurement settings. Default: 10 iterations, 2 warmup. |
| `analyze_versions(repo_path, versions)` | `repo_path: str, versions: List[str]` | Measure energy for each version (checkout, warmup, measure N iterations). Returns `VersionPowerReport` with trend analysis (increasing/decreasing/stable based on 5% threshold). |

---

## Energy

### `greenmining/energy/base.py`

Core abstractions for energy measurement.

#### class `EnergyBackend` (Enum)

Supported backends: `RAPL`, `CODECARBON`, `CPU_METER`.

#### class `EnergyMetrics` (dataclass)

Energy measurement results.

| Field | Type | Description |
|-------|------|-------------|
| `joules` | `float` | Total energy consumed |
| `watts_avg` | `float` | Average power draw |
| `watts_peak` | `float` | Peak power draw |
| `duration_seconds` | `float` | Measurement duration |
| `cpu_energy_joules` | `float` | CPU-specific energy |
| `dram_energy_joules` | `float` | Memory energy |
| `gpu_energy_joules` | `Optional[float]` | GPU energy |
| `carbon_grams` | `Optional[float]` | CO2 equivalent in grams |
| `carbon_intensity` | `Optional[float]` | Grid carbon intensity (gCO2/kWh) |
| `backend` | `str` | Backend name |
| `start_time` / `end_time` | `Optional[datetime]` | Measurement timestamps |

| Property | Description |
|----------|-------------|
| `energy_joules` | Alias for `joules`. |
| `average_power_watts` | Alias for `watts_avg`. |

#### class `CommitEnergyProfile` (dataclass)

Energy profile comparing a commit to its parent: `energy_before`, `energy_after`, `energy_delta`, `energy_regression`, `regression_percentage`.

#### class `EnergyMeter` (ABC)

Abstract base class for all energy measurement backends.

| Method | Description |
|--------|-------------|
| `is_available()` | Check if this backend works on the current system. |
| `start()` | Begin energy measurement. |
| `stop()` | Stop measurement, return `EnergyMetrics`. |
| `measure(func, *args, **kwargs)` | Measure energy of a function call. Returns `(result, EnergyMetrics)`. |
| `measure_command(command, timeout)` | Measure energy of a shell command. |
| `__enter__` / `__exit__` | Context manager support. |

#### `get_energy_meter(backend)`

Factory function. Supported values: `"rapl"`, `"codecarbon"`, `"cpu_meter"`, `"cpu"`, `"auto"`. Auto mode tries RAPL first (most accurate), falls back to CPU meter.

---

### `greenmining/energy/rapl.py`

#### class `RAPLEnergyMeter`

Intel RAPL (Running Average Power Limit) energy measurement for Linux. Reads directly from `/sys/class/powercap/intel-rapl`.

| Method | Description |
|--------|-------------|
| `__init__()` | Discover available RAPL domains (package, core, dram, uncore). |
| `is_available()` | Check if RAPL sysfs interface exists and is readable. |
| `start()` | Record starting energy values for all domains. |
| `stop()` | Calculate energy delta per domain. Handles 32-bit counter wrap-around. Returns `EnergyMetrics` with CPU, DRAM, and GPU (uncore) breakdowns. |
| `get_available_domains()` | List discovered RAPL domain names. |

---

### `greenmining/energy/cpu_meter.py`

#### class `CPUEnergyMeter`

Cross-platform CPU energy estimation. Works on Linux, macOS, and Windows. Estimates power from CPU utilization percentage and TDP.

Power model: `P = P_idle + (P_max - P_idle) * utilization` where idle power is 30% of TDP.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(tdp_watts, sample_interval)` | `tdp_watts: Optional[float], sample_interval: float` | Initialize. Auto-detects TDP from RAPL sysfs on Linux, or uses platform defaults (Linux: 65W, macOS: 30W, Windows: 65W). |
| `is_available()` | none | Always returns True (universal fallback). |
| `start()` | none | Begin measurement, prime psutil. |
| `stop()` | none | Calculate estimated energy from CPU utilization samples. |

---

### `greenmining/energy/codecarbon_meter.py`

#### class `CodeCarbonMeter`

Energy measurement with CO2 tracking via the CodeCarbon library. Provides carbon emissions in addition to energy data.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(project_name, output_dir, save_to_file)` | see params | Initialize CodeCarbon tracker. |
| `is_available()` | none | Check if `codecarbon` package is installed. |
| `start()` | none | Create and start `EmissionsTracker`. |
| `stop()` | none | Stop tracker, extract energy (kWh to joules), emissions (kg to grams), and carbon intensity. Handles CodeCarbon v3.x Energy objects. |
| `get_carbon_intensity()` | none | Query current grid carbon intensity for the configured region. |

---

### `greenmining/energy/carbon_reporter.py`

#### `CARBON_INTENSITY_BY_COUNTRY`

Dictionary of average carbon intensity (gCO2/kWh) for 20 countries. Source: Electricity Maps, IEA.

#### `CLOUD_REGION_INTENSITY`

Dictionary of carbon intensity by cloud provider region for AWS (14 regions), GCP (9 regions), and Azure (8 regions).

#### class `CarbonReport` (dataclass)

Carbon emissions report: total energy (kWh), emissions (kg), carbon intensity, equivalents (tree-months, smartphone charges, km driven).

#### class `CarbonReporter`

Generate carbon footprint reports from energy measurements.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(country_iso, cloud_provider, region)` | see params | Initialize with location. Cloud region intensity takes priority over country average. |
| `generate_report(energy_metrics, analysis_results, total_joules)` | see params | Generate `CarbonReport` from energy data. Converts joules to kWh, applies carbon intensity, calculates equivalents. |
| `get_carbon_intensity()` | none | Get the configured carbon intensity value. |
| `get_supported_countries()` | static | List supported country ISO codes. |
| `get_supported_cloud_regions(provider)` | static | List supported regions for a cloud provider. |

---

## Controllers

### `greenmining/controllers/repository_controller.py`

#### class `RepositoryController`

Orchestrates repository fetching operations using the GraphQL fetcher and configuration.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `__init__(config)` | `config: Config` | Initialize with Config object. Creates `GitHubGraphQLFetcher`. |
| `fetch_repositories(max_repos, min_stars, languages, keywords, created_after, created_before, pushed_after, pushed_before)` | see params | Fetch repositories via GraphQL, save to JSON file. Parameters default to Config values. |
| `load_repositories()` | none | Load previously fetched repositories from JSON file. |
| `get_repository_stats(repositories)` | `repositories: list[Repository]` | Compute statistics: total count, by-language breakdown, total/avg stars, top repository. |

---

## Presenters

### `greenmining/presenters/console_presenter.py`

#### class `ConsolePresenter`

Handles formatted console output using tabulate and colorama.

| Method | Parameters | Description |
|--------|-----------|-------------|
| `show_banner()` | static | Display application banner. |
| `show_repositories(repositories, limit)` | static | Display repository table (name, language, stars, description). |
| `show_commit_stats(stats)` | static | Display commit statistics table. |
| `show_analysis_results(results)` | static | Display analysis results summary. |
| `show_pattern_distribution(patterns, limit)` | static | Display top N green patterns with counts and percentages. |
| `show_pipeline_status(status)` | static | Display pipeline phase status. |
| `show_progress_message(phase, current, total)` | static | Display progress percentage. |
| `show_error(message)` | static | Print error in red. |
| `show_success(message)` | static | Print success in green. |
| `show_warning(message)` | static | Print warning in yellow. |
