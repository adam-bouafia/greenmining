# Python API Reference

Use GreenMining programmatically in your Python scripts.

---

## Quick Import

```python
from greenmining import (
    GSF_PATTERNS,        # Dict of 124 GSF patterns
    GREEN_KEYWORDS,      # List of 332 green keywords
    is_green_aware,      # Check if message is green-aware
    get_pattern_by_keywords,  # Get matched patterns
    fetch_repositories,  # Fetch repos from GitHub
    Config,              # Configuration class
)
```

---

## Core Functions

### is_green_aware()

Check if a commit message indicates green software awareness.

```python
def is_green_aware(commit_message: str) -> bool
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `commit_message` | str | The commit message to analyze |

**Returns:** `bool` - True if message contains green keywords

**Example:**

```python
from greenmining import is_green_aware

# Returns True
is_green_aware("Optimize Redis caching for better performance")
is_green_aware("Enable gzip compression on API responses")
is_green_aware("Implement async batch processing")

# Returns False
is_green_aware("Fix typo in README")
is_green_aware("Update dependencies")
is_green_aware("Refactor variable names")
```

---

### get_pattern_by_keywords()

Find GSF patterns that match a commit message.

```python
def get_pattern_by_keywords(commit_message: str) -> list[str]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `commit_message` | str | The commit message to analyze |

**Returns:** `list[str]` - List of matched pattern names

**Example:**

```python
from greenmining import get_pattern_by_keywords

patterns = get_pattern_by_keywords("Implement Redis caching layer")
print(patterns)
# Output: ['Cache Static Data']

patterns = get_pattern_by_keywords("Enable gzip compression for API responses")
print(patterns)
# Output: ['Compress Transmitted Data', 'Enable Text Compression']

patterns = get_pattern_by_keywords("Fix typo")
print(patterns)
# Output: []
```

---

### fetch_repositories()

Fetch repositories from GitHub matching search criteria.

```python
def fetch_repositories(
    github_token: str,
    max_repos: int = 100,
    min_stars: int = 100,
    languages: list = None,
    keywords: str = "microservices"
) -> list
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `github_token` | str | (required) | GitHub personal access token |
| `max_repos` | int | 100 | Maximum repositories to fetch |
| `min_stars` | int | 100 | Minimum star count |
| `languages` | list | None | Filter by languages |
| `keywords` | str | "microservices" | Search keywords |

**Returns:** `list` - List of Repository objects

**Example:**

```python
from greenmining import fetch_repositories

repos = fetch_repositories(
    github_token="ghp_xxxx",
    max_repos=10,
    min_stars=500,
    keywords="kubernetes",
    languages=["Python", "Go"]
)

for repo in repos:
    print(f"{repo.full_name}: {repo.stars} stars")
```

---

## Data Structures

### GSF_PATTERNS

Dictionary containing all 124 Green Software Foundation patterns.

```python
from greenmining import GSF_PATTERNS

# Structure
GSF_PATTERNS = {
    "pattern_id": {
        "name": "Pattern Name",
        "category": "category_name",
        "keywords": ["keyword1", "keyword2"],
        "description": "Pattern description",
        "sci_impact": "Impact on software carbon intensity"
    },
    ...
}
```

**Example Usage:**

```python
from greenmining import GSF_PATTERNS

# Get pattern count
print(f"Total patterns: {len(GSF_PATTERNS)}")  # 124

# Get all categories
categories = set(p["category"] for p in GSF_PATTERNS.values())
print(f"Categories: {categories}")
# {'cloud', 'web', 'ai', 'caching', 'async', 'database', ...}

# Find patterns by category
cloud_patterns = [
    p["name"] for p in GSF_PATTERNS.values() 
    if p["category"] == "cloud"
]
print(f"Cloud patterns: {len(cloud_patterns)}")  # 40+

# Get pattern details
cache_pattern = GSF_PATTERNS["cache_static_data"]
print(f"Name: {cache_pattern['name']}")
print(f"Keywords: {cache_pattern['keywords']}")
```

---

### GREEN_KEYWORDS

List of 332 keywords indicating green software practices.

```python
from greenmining import GREEN_KEYWORDS

print(f"Total keywords: {len(GREEN_KEYWORDS)}")  # 332

# Sample keywords
print(GREEN_KEYWORDS[:10])
# ['energy', 'power', 'carbon', 'emission', 'footprint', 
#  'sustainability', 'sustainable', 'green', 'efficient', 'efficiency']
```

### analyze_repositories()

Analyze multiple repositories from URLs with optional parallel processing.

```python
def analyze_repositories(
    urls: list,
    max_commits: int = 500,
    parallel_workers: int = 1,
    output_format: str = "dict",
    energy_tracking: bool = False,
    energy_backend: str = "rapl",
    method_level_analysis: bool = False,
    include_source_code: bool = False,
    ssh_key_path: str = None,
    github_token: str = None,
) -> list
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `urls` | list | (required) | List of GitHub repository URLs |
| `max_commits` | int | 500 | Maximum commits per repository |
| `parallel_workers` | int | 1 | Concurrent analysis workers |
| `energy_tracking` | bool | False | Enable energy measurement |
| `energy_backend` | str | "rapl" | Energy backend (rapl, codecarbon, cpu_meter, auto) |
| `method_level_analysis` | bool | False | Include per-method metrics |
| `include_source_code` | bool | False | Include source code before/after |
| `ssh_key_path` | str | None | SSH key for private repos |
| `github_token` | str | None | GitHub token for private HTTPS repos |

**Example:**

```python
from greenmining import analyze_repositories

results = analyze_repositories(
    urls=[
        "https://github.com/kubernetes/kubernetes",
        "https://github.com/istio/istio",
    ],
    max_commits=100,
    parallel_workers=4,
    energy_tracking=True,
    energy_backend="auto",
)

for result in results:
    print(f"{result.name}: {result.green_commit_rate:.1%} green")
```

---

## Service Classes

### DataAnalyzer

Analyze commits for green software patterns.

```python
from greenmining.services.data_analyzer import DataAnalyzer

analyzer = DataAnalyzer(
    enable_diff_analysis=False,  # Analyze code diffs
    patterns=None,               # Custom patterns (default: GSF_PATTERNS)
    batch_size=10                # Commits per batch
)
```

**Methods:**

```python
# Analyze a single commit
result = analyzer.analyze_commit(commit_dict)

# Analyze multiple commits
results = analyzer.analyze_commits(commits_list)

# Save results to file
analyzer.save_results(results, "output.json")
```

**Example:**

```python
from greenmining.services.data_analyzer import DataAnalyzer

analyzer = DataAnalyzer(enable_diff_analysis=True)

commit = {
    "sha": "abc123",
    "message": "Implement Redis caching for user sessions",
    "author": "developer",
    "date": "2024-01-15T10:00:00Z"
}

result = analyzer.analyze_commit(commit)
print(f"Green-aware: {result['green_aware']}")
print(f"Patterns: {result['patterns']}")
```

---

### DataAggregator

Aggregate analysis results with statistics.

```python
from greenmining.services.data_aggregator import DataAggregator

aggregator = DataAggregator(
    enable_stats=True,            # Statistical analysis
    enable_temporal=True,         # Temporal trends
    temporal_granularity="quarter"  # day/week/month/quarter/year
)
```

**Methods:**

```python
# Aggregate results
aggregated = aggregator.aggregate(analysis_results, repositories)

# Save to files
aggregator.save_results(aggregated, "stats.json", "stats.csv", analysis_results)

# Print summary
aggregator.print_summary(aggregated)
```

**Example:**

```python
from greenmining.services.data_aggregator import DataAggregator

aggregator = DataAggregator(
    enable_stats=True,
    enable_temporal=True,
    temporal_granularity="month"
)

# Assuming analysis_results and repositories are already populated
aggregated = aggregator.aggregate(analysis_results, repositories)

print(f"Total commits: {aggregated['summary']['total_commits']}")
print(f"Green-aware: {aggregated['summary']['green_aware_percentage']}%")
```

---

### LocalRepoAnalyzer

Analyze repositories directly from GitHub URLs.

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer(
    clone_path="/tmp/greenmining_repos",  # Clone directory
    max_commits=500,                       # Max commits per repo
    days_back=730,                         # How far back to analyze
    skip_merges=True,                      # Skip merge commits
    compute_process_metrics=True,          # Compute process metrics
    cleanup_after=True,                    # Delete after analysis
    ssh_key_path=None,                     # SSH key for private repos
    github_token=None,                     # GitHub token for private repos
    energy_tracking=False,                 # Enable energy measurement
    energy_backend="rapl",                 # Energy backend
    method_level_analysis=False,           # Per-method metrics
    include_source_code=False,             # Source code before/after
    process_metrics="standard",            # "standard" or "full"
)
```

**Methods:**

```python
# Analyze single repository
result = analyzer.analyze_repository("https://github.com/owner/repo")

# Analyze multiple repositories (with parallelism)
results = analyzer.analyze_repositories(
    urls=["https://github.com/org/repo1", "https://github.com/org/repo2"],
    parallel_workers=4,
)
```

**Example: Basic analysis**

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer(cleanup_after=True)
result = analyzer.analyze_repository("https://github.com/pallets/flask")

print(f"Repository: {result.name}")
print(f"Commits analyzed: {result.total_commits}")
print(f"Green-aware: {result.green_commits} ({result.green_commit_rate:.1%})")

for commit in result.commits[:5]:
    if commit.green_aware:
        print(f"  {commit.message[:50]}...")
```

**Example: Private repository with energy tracking**

```python
analyzer = LocalRepoAnalyzer(
    github_token="ghp_xxxx",
    energy_tracking=True,
    energy_backend="auto",
    method_level_analysis=True,
)

result = analyzer.analyze_repository("https://github.com/company/private-repo")
print(f"Energy consumed: {result.energy_metrics['joules']:.2f} J")

for commit in result.commits:
    for method in commit.methods:
        print(f"  {method.name}: complexity={method.complexity}")
```

**Example: Batch parallel analysis**

```python
analyzer = LocalRepoAnalyzer(max_commits=100)
results = analyzer.analyze_repositories(
    urls=[
        "https://github.com/kubernetes/kubernetes",
        "https://github.com/istio/istio",
        "https://github.com/envoyproxy/envoy",
    ],
    parallel_workers=3,
)

for result in results:
    print(f"{result.name}: {result.green_commit_rate:.1%} green")
```

---

### ReportGenerator

Generate Markdown reports from analysis results.

```python
from greenmining.services.reports import ReportGenerator

generator = ReportGenerator()
```

**Methods:**

```python
# Generate full report
report = generator.generate_report(aggregated_data)

# Save to file
generator.save_report(report, "report.md")
```

---

## Analyzer Classes

### StatisticalAnalyzer

Compute statistical metrics on analysis results.

```python
from greenmining.analyzers.statistical_analyzer import StatisticalAnalyzer

analyzer = StatisticalAnalyzer()

# Pattern correlations
correlations = analyzer.analyze_pattern_correlations(analysis_results)

# Effect sizes
effect_sizes = analyzer.analyze_effect_sizes(analysis_results)

# Descriptive statistics
descriptive = analyzer.get_descriptive_statistics(analysis_results)
```

---

### TemporalAnalyzer

Analyze patterns over time.

```python
from greenmining.analyzers.temporal_analyzer import TemporalAnalyzer

analyzer = TemporalAnalyzer(granularity="quarter")

# Group commits by period
periods = analyzer.group_commits_by_period(commits)

# Analyze trends
trends = analyzer.analyze_trends(periods)

# Pattern evolution
evolution = analyzer.analyze_pattern_evolution(commits)
```

---

### QualitativeAnalyzer

Generate validation samples for manual review.

```python
from greenmining.analyzers.qualitative_analyzer import QualitativeAnalyzer

analyzer = QualitativeAnalyzer(
    sample_size=30,
    stratify_by="pattern"  # pattern/repository/time/random
)

# Generate samples
samples = analyzer.generate_validation_samples(analysis_results)

# Export for review
analyzer.export_samples_for_review(samples, "validation_samples.csv")
```

---

### CodeDiffAnalyzer

Analyze code changes for green patterns.

```python
from greenmining.analyzers.code_diff_analyzer import CodeDiffAnalyzer

analyzer = CodeDiffAnalyzer()

# Check if file is analyzable
is_code = analyzer.is_code_file("app.py")  # True

# Analyze diff content
patterns = analyzer.detect_patterns_in_diff(diff_text)
```

---

### PowerRegressionDetector

Identify commits that caused power consumption regressions by running a test command
at each commit and measuring energy usage.

```python
from greenmining.analyzers import PowerRegressionDetector

detector = PowerRegressionDetector(
    test_command="pytest tests/ -x",
    energy_backend="rapl",
    threshold_percent=5.0,
    iterations=5,
    warmup_iterations=1,
)

regressions = detector.detect(
    repo_path="/path/to/repo",
    baseline_commit="v1.0.0",
    target_commit="HEAD",
)

for regression in regressions:
    print(f"Commit {regression.sha[:8]}: +{regression.power_increase:.1f}%")
    print(f"  Message: {regression.message}")
```

**Constructor Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `test_command` | str | `"pytest tests/ -x"` | Shell command to run for measurement |
| `energy_backend` | str | `"rapl"` | Energy backend (rapl, codecarbon, cpu_meter, auto) |
| `threshold_percent` | float | `5.0` | Minimum % increase to flag as regression |
| `iterations` | int | `5` | Measurement iterations per commit |
| `warmup_iterations` | int | `1` | Warmup runs before measuring |

**PowerRegression Output:**

| Field | Type | Description |
|-------|------|-------------|
| `sha` | str | Commit SHA |
| `message` | str | Commit message |
| `author` | str | Commit author |
| `date` | str | Commit date |
| `power_before` | float | Average power before (watts) |
| `power_after` | float | Average power after (watts) |
| `power_increase` | float | Percentage increase |
| `energy_before` | float | Energy before (joules) |
| `energy_after` | float | Energy after (joules) |
| `is_regression` | bool | True if above threshold |

---

### MetricsPowerCorrelator

Correlate code metrics (complexity, NLOC, churn) with power consumption using
Pearson and Spearman correlation coefficients.

```python
from greenmining.analyzers import MetricsPowerCorrelator

correlator = MetricsPowerCorrelator(significance_level=0.05)
correlator.fit(
    metrics=["complexity", "nloc", "code_churn"],
    metrics_values={
        "complexity": [...],
        "nloc": [...],
        "code_churn": [...],
    },
    power_measurements=[...],
)

# Access results
for name, result in correlator.get_results().items():
    print(f"{name}: pearson={result.pearson_r:.3f}, spearman={result.spearman_r:.3f}")
    print(f"  Significant: {result.significant}, Strength: {result.strength}")

# Feature importance ranking
for name, importance in correlator.feature_importance.items():
    print(f"{name}: {importance:.3f}")
```

**Constructor Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `significance_level` | float | `0.05` | P-value threshold for significance |

**CorrelationResult Output:**

| Field | Type | Description |
|-------|------|-------------|
| `metric_name` | str | Name of the metric |
| `pearson_r` | float | Pearson correlation coefficient |
| `pearson_p` | float | Pearson p-value |
| `spearman_r` | float | Spearman rank correlation |
| `spearman_p` | float | Spearman p-value |
| `significant` | bool | True if p < significance_level |
| `strength` | str | none, weak, moderate, strong |

---

### VersionPowerAnalyzer

Compare energy consumption across software versions by checking out tags/branches
and running a test suite at each version.

```python
from greenmining.analyzers import VersionPowerAnalyzer

analyzer = VersionPowerAnalyzer(
    test_command="pytest tests/",
    energy_backend="rapl",
    iterations=10,
    warmup_iterations=2,
)

report = analyzer.analyze_versions(
    repo_path="/path/to/repo",
    versions=["v1.0", "v1.1", "v1.2", "v2.0"],
)

print(report.summary())
print(f"Trend: {report.trend}")            # increasing, decreasing, stable
print(f"Most efficient: {report.most_efficient}")
print(f"Total change: {report.total_change_percent:.1f}%")

for v in report.versions:
    print(f"  {v.version}: {v.power_watts_avg:.2f}W (std: {v.energy_std:.4f})")
```

**Constructor Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `test_command` | str | `"pytest tests/"` | Shell command to run per version |
| `energy_backend` | str | `"rapl"` | Energy backend |
| `iterations` | int | `5` | Measurement iterations per version |
| `warmup_iterations` | int | `1` | Warmup runs before measuring |

**VersionPowerReport Output:**

| Field | Type | Description |
|-------|------|-------------|
| `versions` | list | List of VersionPowerProfile objects |
| `trend` | str | increasing, decreasing, or stable |
| `total_change_percent` | float | % change from first to last version |
| `most_efficient` | str | Version tag with lowest power |
| `least_efficient` | str | Version tag with highest power |

**VersionPowerProfile Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `version` | str | Version tag or branch name |
| `commit_sha` | str | Resolved commit SHA |
| `energy_joules` | float | Average energy per run |
| `power_watts_avg` | float | Average power draw |
| `duration_seconds` | float | Average test duration |
| `iterations` | int | Number of measurement iterations |
| `energy_std` | float | Standard deviation across iterations |

---

### CarbonReporter

Generate carbon footprint reports from energy measurements. Supports 20+ countries
and major cloud providers (AWS, GCP, Azure).

```python
from greenmining.energy import CarbonReporter

reporter = CarbonReporter(
    country_iso="USA",
    cloud_provider="aws",
    region="us-east-1",
)

report = reporter.generate_report(total_joules=1000.0)
print(f"CO2 emissions: {report.total_emissions_kg:.4f} kg")
print(f"Equivalent: {report.tree_months:.1f} tree-months")
print(report.summary())
```

---

## Configuration Class

```python
from greenmining.config import Config

config = Config()

# Access configuration values
print(config.MAX_REPOS)           # 100
print(config.COMMITS_PER_REPO)    # 1000
print(config.SUPPORTED_LANGUAGES) # ['Python', 'Java', ...]
print(config.OUTPUT_DIR)          # 'data'

# URL Analysis options
print(config.REPOSITORY_URLS)     # []
print(config.CLONE_PATH)          # '/tmp/greenmining_repos'

# Energy options
print(config.ENERGY_ENABLED)      # False
print(config.ENERGY_BACKEND)      # 'rapl'

# Process metric options
print(config.PROCESS_METRICS_ENABLED)  # True
print(config.DMM_ENABLED)              # True
```

---

## Complete Example

```python
#!/usr/bin/env python3
"""Complete GreenMining analysis workflow."""

from greenmining import GSF_PATTERNS, is_green_aware, get_pattern_by_keywords
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer
from greenmining.services.data_aggregator import DataAggregator
from greenmining.services.reports import ReportGenerator

# 1. Analyze repository
analyzer = LocalRepoAnalyzer(cleanup_after=True)
result = analyzer.analyze_repository(
    repo_url="https://github.com/pallets/flask",
    max_commits=200
)

print(f"Analyzed {result['total_commits']} commits")
print(f"Green-aware: {result['green_aware_count']} ({result['green_aware_percentage']:.1f}%)")

# 2. Aggregate results
aggregator = DataAggregator(enable_stats=True, enable_temporal=True)
aggregated = aggregator.aggregate(
    analysis_results=result['commits'],
    repositories=[result['repository']]
)

# 3. Generate report
generator = ReportGenerator()
report = generator.generate_report(aggregated)
generator.save_report(report, "flask_analysis.md")

print("Report saved to flask_analysis.md")
```

---

## Next Steps

- [URL Analysis](url-analysis.md) - Deep dive into URL-based analysis
- [Energy Measurement](energy.md) - Power profiling with RAPL/CodeCarbon
- [GSF Patterns Reference](../reference/patterns.md) - All 124 patterns
