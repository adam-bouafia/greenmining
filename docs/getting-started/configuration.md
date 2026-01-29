# Configuration

GreenMining can be configured via environment variables, `.env` files, or programmatically.

---

## Configuration Methods

### Method 1: Environment Variables

Set variables directly in your shell:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
export MAX_REPOS=50
export MIN_STARS=500
export ENABLE_TEMPORAL=true
```

### Method 2: .env File

Create a `.env` file in your project directory:

```bash
# Required
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Repository Fetching
MAX_REPOS=100
MIN_STARS=100
SUPPORTED_LANGUAGES=Python,Java,Go,JavaScript,TypeScript
SEARCH_KEYWORDS=microservices

# Commit Extraction
COMMITS_PER_REPO=1000
EXCLUDE_MERGE_COMMITS=true
EXCLUDE_BOT_COMMITS=true

# Analysis Features
ENABLE_DIFF_ANALYSIS=false
BATCH_SIZE=10

# Temporal Analysis
ENABLE_TEMPORAL=true
TEMPORAL_GRANULARITY=quarter
ENABLE_STATS=true

# Output
OUTPUT_DIR=./data
REPORT_FORMAT=markdown
```

### Method 3: Python Config Object

```python
from greenmining.config import Config

config = Config()

# Override settings
config.MAX_REPOS = 50
config.COMMITS_PER_REPO = 200
config.MIN_STARS = 500
```

---

## Configuration Options Reference

### GitHub API

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `GITHUB_TOKEN` | string | (required) | GitHub personal access token |

### Repository Fetching

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `MAX_REPOS` | int | 100 | Maximum repositories to fetch |
| `MIN_STARS` | int | 100 | Minimum GitHub stars required |
| `SUPPORTED_LANGUAGES` | list | Python,Java,Go,... | Language filter (comma-separated) |
| `SEARCH_KEYWORDS` | string | microservices | Search keywords for GitHub API |

### URL Analysis

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `REPOSITORY_URLS` | list | [] | List of repository URLs to analyze |
| `CLONE_PATH` | string | /tmp/greenmining_repos | Directory for cloning repositories |
| `CLEANUP_AFTER_ANALYSIS` | bool | true | Delete cloned repos after analysis |

### Commit Extraction

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `COMMITS_PER_REPO` | int | 1000 | Maximum commits per repository |
| `EXCLUDE_MERGE_COMMITS` | bool | true | Skip merge commits |
| `EXCLUDE_BOT_COMMITS` | bool | true | Skip bot commits |
| `MIN_MESSAGE_LENGTH` | int | 10 | Minimum commit message length |

### Analysis Features

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ENABLE_DIFF_ANALYSIS` | bool | false | Analyze code diffs (slower) |
| `BATCH_SIZE` | int | 10 | Commits per batch |

### PyDriller Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `PROCESS_METRICS_ENABLED` | bool | true | Compute process metrics |
| `STRUCTURAL_METRICS_ENABLED` | bool | true | Compute structural metrics |
| `DMM_ENABLED` | bool | true | Delta Maintainability Model |

### Statistical Analysis

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ENABLE_STATS` | bool | false | Enable statistical analysis |
| `ENABLE_TEMPORAL` | bool | false | Enable temporal trend analysis |
| `TEMPORAL_GRANULARITY` | string | quarter | day/week/month/quarter/year |

### Energy Measurement

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ENERGY_ENABLED` | bool | false | Enable energy measurement |
| `ENERGY_BACKEND` | string | rapl | rapl, codecarbon, or cpu_meter |
| `CARBON_TRACKING` | bool | false | Track carbon emissions |
| `COUNTRY_ISO` | string | USA | Country for carbon calculations |

### Output Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `OUTPUT_DIR` | string | ./data | Output directory path |
| `REPOS_FILE` | string | repositories.json | Repository data filename |
| `COMMITS_FILE` | string | commits.json | Commits data filename |
| `ANALYSIS_FILE` | string | analysis_results.json | Analysis results filename |
| `STATS_FILE` | string | aggregated_statistics.json | Statistics filename |
| `REPORT_FILE` | string | green_analysis.md | Report filename |

---

## YAML Configuration

For advanced configuration, use a YAML file:

**config/config.yaml:**

```yaml
# GreenMining Configuration
version: "2.0"

search:
  keywords: ["microservices", "kubernetes"]
  languages: ["Python", "Go", "Java"]
  min_stars: 100
  max_repos: 100
  
  temporal:
    created_after: "2020-01-01"
    created_before: "2025-12-31"
    pushed_after: "2023-01-01"

detection:
  methods:
    keyword:
      enabled: true
      confidence_weight: 1.0
    
    diff_analysis:
      enabled: true
      confidence_weight: 0.8

analysis:
  statistical:
    enabled: true
    methods:
      - chi_square
      - correlation_analysis
      - temporal_trends
      - effect_sizes
```

---

## Configuration Precedence

Configuration values are loaded in this order (later overrides earlier):

1. **Default values** in `Config` class
2. **YAML config file** if specified
3. **`.env` file** in current directory
4. **Environment variables**
5. **Python Config overrides**

---

## Validating Configuration

Check current configuration in Python:

```python
from greenmining.config import Config

config = Config()

# Check settings
print(f"GITHUB_TOKEN: {'***configured***' if config.GITHUB_TOKEN else 'Not set'}")
print(f"MAX_REPOS: {config.MAX_REPOS}")
print(f"COMMITS_PER_REPO: {config.COMMITS_PER_REPO}")
print(f"OUTPUT_DIR: {config.OUTPUT_DIR}")
print(f"ENABLE_TEMPORAL: {config.ENABLE_TEMPORAL}")
print(f"TEMPORAL_GRANULARITY: {config.TEMPORAL_GRANULARITY}")
```

---

## Next Steps

- [Quick Start](quickstart.md) - Get started with examples
- [Python API](../user-guide/api.md) - Programmatic configuration
- [Config Options Reference](../reference/config-options.md) - Full reference
