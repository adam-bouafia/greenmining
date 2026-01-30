# Configuration Options Reference

Complete reference for all GreenMining configuration options.

---

## Configuration Methods

GreenMining supports multiple configuration methods:

1. **Environment variables** - `export OPTION=value`
2. **`.env` file** - Key-value pairs in project root
3. **Python Config object** - Programmatic configuration

### Precedence Order

Later sources override earlier ones:

1. Default values (lowest priority)
2. `.env` file
3. Environment variables
4. Python Config overrides (highest priority)

---

## GitHub API Options

### GITHUB_TOKEN

GitHub personal access token for API access.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Default** | (none - required) |
| **Environment** | `GITHUB_TOKEN` |
| **Required** | Yes (for fetch operations) |

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

---

## Repository Fetching Options

### MAX_REPOS

Maximum number of repositories to fetch from GitHub.

| Property | Value |
|----------|-------|
| **Type** | integer |
| **Default** | 100 |
| **Environment** | `MAX_REPOS` |

```python
from greenmining import fetch_repositories

repos = fetch_repositories(github_token=token, max_repos=50)
```

### MIN_STARS

Minimum GitHub star count required for repositories.

| Property | Value |
|----------|-------|
| **Type** | integer |
| **Default** | 100 |
| **Environment** | `MIN_STARS` |

```python
repos = fetch_repositories(github_token=token, min_stars=500)
```

### SUPPORTED_LANGUAGES

Programming languages to filter repositories.

| Property | Value |
|----------|-------|
| **Type** | list (comma-separated) |
| **Default** | Python,Java,Go,JavaScript,TypeScript,C#,Rust |
| **Environment** | `SUPPORTED_LANGUAGES` |

```python
repos = fetch_repositories(github_token=token, languages=["Python", "Go", "Rust"])
```

### SEARCH_KEYWORDS

Keywords for GitHub repository search.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Default** | microservices |
| **Environment** | `SEARCH_KEYWORDS` |

```python
repos = fetch_repositories(github_token=token, keywords="kubernetes cloud-native")
```

---

## URL Analysis Options

### REPOSITORY_URLS

List of repository URLs to analyze directly.

| Property | Value |
|----------|-------|
| **Type** | list |
| **Default** | [] |
| **Environment** | `REPOSITORY_URLS` (comma-separated) |

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer(max_commits=100)
result = analyzer.analyze_repository("https://github.com/org/repo")
```

### CLONE_PATH

Directory where repositories are cloned for analysis.

| Property | Value |
|----------|-------|
| **Type** | string (path) |
| **Default** | /tmp/greenmining_repos |
| **Environment** | `CLONE_PATH` |

```bash
export CLONE_PATH=/var/data/greenmining
```

### CLEANUP_AFTER_ANALYSIS

Whether to delete cloned repositories after analysis.

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | true |
| **Environment** | `CLEANUP_AFTER_ANALYSIS` |

```bash
export CLEANUP_AFTER_ANALYSIS=false
```

---

## Commit Extraction Options

### COMMITS_PER_REPO

Maximum commits to extract per repository.

| Property | Value |
|----------|-------|
| **Type** | integer |
| **Default** | 1000 |
| **Environment** | `COMMITS_PER_REPO` |

```python
from greenmining.services.commit_extractor import CommitExtractor

extractor = CommitExtractor()
extractor.max_commits = 500
```

### EXCLUDE_MERGE_COMMITS

Skip merge commits during extraction.

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | true |
| **Environment** | `EXCLUDE_MERGE_COMMITS` |

```bash
export EXCLUDE_MERGE_COMMITS=false
```

### EXCLUDE_BOT_COMMITS

Skip commits from bot accounts.

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | true |
| **Environment** | `EXCLUDE_BOT_COMMITS` |

```bash
export EXCLUDE_BOT_COMMITS=false
```

### MIN_MESSAGE_LENGTH

Minimum commit message length to include.

| Property | Value |
|----------|-------|
| **Type** | integer |
| **Default** | 10 |
| **Environment** | `MIN_MESSAGE_LENGTH` |

```bash
export MIN_MESSAGE_LENGTH=20
```

---

## Analysis Options

### ENABLE_DIFF_ANALYSIS

Enable code diff analysis for pattern detection.

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | false |
| **Environment** | `ENABLE_DIFF_ANALYSIS` |

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer(enable_diff_analysis=True)
```

### BATCH_SIZE

Number of commits to process per batch.

| Property | Value |
|----------|-------|
| **Type** | integer |
| **Default** | 10 |
| **Environment** | `BATCH_SIZE` |

```python
from greenmining.services.data_analyzer import DataAnalyzer

analyzer = DataAnalyzer()
analyzer.batch_size = 50
```

---

## Process Metrics Options

### PROCESS_METRICS_ENABLED

Compute process metrics (code churn, change set, etc.).

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | true |
| **Environment** | `PROCESS_METRICS_ENABLED` |

```bash
export PROCESS_METRICS_ENABLED=true
```

### STRUCTURAL_METRICS_ENABLED

Compute structural metrics (complexity, lines of code).

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | true |
| **Environment** | `STRUCTURAL_METRICS_ENABLED` |

```bash
export STRUCTURAL_METRICS_ENABLED=true
```

### DMM_ENABLED

Enable Delta Maintainability Model metrics.

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | true |
| **Environment** | `DMM_ENABLED` |

```bash
export DMM_ENABLED=true
```

---

## Statistical Analysis Options

### ENABLE_STATS

Enable statistical analysis (correlations, effect sizes).

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | false |
| **Environment** | `ENABLE_STATS` |

```python
from greenmining.services.data_aggregator import DataAggregator

aggregator = DataAggregator(enable_stats=True)
```

### ENABLE_TEMPORAL

Enable temporal trend analysis.

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | false |
| **Environment** | `ENABLE_TEMPORAL` |

```python
aggregator = DataAggregator(enable_temporal=True)
```

### TEMPORAL_GRANULARITY

Time period granularity for temporal analysis.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Default** | quarter |
| **Options** | day, week, month, quarter, year |
| **Environment** | `TEMPORAL_GRANULARITY` |

```python
aggregator = DataAggregator(temporal_granularity="month")
```

---

## Energy Measurement Options

### ENERGY_ENABLED

Enable energy measurement during analysis.

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | false |
| **Environment** | `ENERGY_ENABLED` |

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer(
    energy_enabled=True,
    energy_backend="rapl"
)
```

### ENERGY_BACKEND

Energy measurement backend to use.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Default** | rapl |
| **Options** | rapl, codecarbon |
| **Environment** | `ENERGY_BACKEND` |

```python
analyzer = LocalRepoAnalyzer(
    energy_enabled=True,
    energy_backend="codecarbon"
)
```

### CARBON_TRACKING

Enable carbon emissions tracking (CodeCarbon only).

| Property | Value |
|----------|-------|
| **Type** | boolean |
| **Default** | false |
| **Environment** | `CARBON_TRACKING` |

```bash
export CARBON_TRACKING=true
```

### COUNTRY_ISO

ISO country code for carbon intensity calculations.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Default** | USA |
| **Environment** | `COUNTRY_ISO` |

```bash
export COUNTRY_ISO=DEU  # Germany
```

---

## Output Options

### OUTPUT_DIR

Directory for output files.

| Property | Value |
|----------|-------|
| **Type** | string (path) |
| **Default** | ./data |
| **Environment** | `OUTPUT_DIR` |

```bash
export OUTPUT_DIR=/var/results/greenmining
```

### REPOS_FILE

Filename for repository data.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Default** | repositories.json |
| **Environment** | `REPOS_FILE` |

### COMMITS_FILE

Filename for commit data.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Default** | commits.json |
| **Environment** | `COMMITS_FILE` |

### ANALYSIS_FILE

Filename for analysis results.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Default** | analysis_results.json |
| **Environment** | `ANALYSIS_FILE` |

### STATS_FILE

Filename for aggregated statistics.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Default** | aggregated_statistics.json |
| **Environment** | `STATS_FILE` |

### REPORT_FILE

Filename for Markdown report.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Default** | green_analysis.md |
| **Environment** | `REPORT_FILE` |

---

## Sample .env File

Complete `.env` configuration:

```bash
# Required
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Repository Fetching
MAX_REPOS=100
MIN_STARS=100
SUPPORTED_LANGUAGES=Python,Java,Go,JavaScript,TypeScript
SEARCH_KEYWORDS=microservices

# URL Analysis
CLONE_PATH=/tmp/greenmining_repos
CLEANUP_AFTER_ANALYSIS=true

# Commit Extraction
COMMITS_PER_REPO=1000
EXCLUDE_MERGE_COMMITS=true
EXCLUDE_BOT_COMMITS=true
MIN_MESSAGE_LENGTH=10

# Analysis
ENABLE_DIFF_ANALYSIS=false
BATCH_SIZE=10

# Process Metrics
PROCESS_METRICS_ENABLED=true
STRUCTURAL_METRICS_ENABLED=true
DMM_ENABLED=true

# Statistical Analysis
ENABLE_STATS=true
ENABLE_TEMPORAL=true
TEMPORAL_GRANULARITY=quarter

# Energy Measurement
ENERGY_ENABLED=false
ENERGY_BACKEND=rapl
CARBON_TRACKING=false
COUNTRY_ISO=USA

# Output
OUTPUT_DIR=./data
REPORT_FILE=green_analysis.md
```

---

## Python Config Class

```python
from greenmining.config import Config

config = Config()

# Access all options
print(f"MAX_REPOS: {config.MAX_REPOS}")
print(f"COMMITS_PER_REPO: {config.COMMITS_PER_REPO}")
print(f"SUPPORTED_LANGUAGES: {config.SUPPORTED_LANGUAGES}")
print(f"CLONE_PATH: {config.CLONE_PATH}")
print(f"ENERGY_ENABLED: {config.ENERGY_ENABLED}")
print(f"ENERGY_BACKEND: {config.ENERGY_BACKEND}")

# Override at runtime
config.MAX_REPOS = 50
config.ENABLE_TEMPORAL = True
```

---

## Next Steps

- [GSF Patterns](patterns.md) - Pattern reference
- [Python API](../user-guide/api.md) - Programmatic configuration
- [Energy Measurement](../user-guide/energy.md) - Energy tracking guide
