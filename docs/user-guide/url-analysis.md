# URL Analysis

Analyze GitHub repositories directly by URL.

---

## Overview

URL analysis allows you to analyze any GitHub repository without using the GitHub API rate limits. GreenMining clones repositories locally and extracts commit data with full diff information.

### Benefits

- **No GitHub API limits** - Clone and analyze directly
- **Full commit data** - Access diffs, modified files, metrics
- **Process metrics** - Code churn, change set size, contributor count
- **DMM metrics** - Delta Maintainability Model scores
- **Method-level analysis** - Per-function complexity via Lizard
- **Historical analysis** - Analyze any date range

---

## Python API

### LocalRepoAnalyzer

The main class for URL-based analysis.

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer(
    clone_path="/tmp/greenmining_repos",  # Where to clone
    cleanup_after=True                     # Delete after analysis
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `clone_path` | str | /tmp/greenmining_repos | Directory for cloning |
| `cleanup_after` | bool | True | Delete cloned repo after analysis |

---

### Single Repository Analysis

Analyze a single repository.

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer
from datetime import datetime

analyzer = LocalRepoAnalyzer()
result = analyzer.analyze_repository(
    repo_url="https://github.com/pallets/flask",
    max_commits=200,
    since_date=datetime(2024, 1, 1),
    to_date=datetime(2024, 12, 31)
)

print(f"Total commits: {result['total_commits']}")
print(f"Green-aware: {result['green_aware_percentage']:.1f}%")
```

### Multiple Repositories

```python
repos = [
    "https://github.com/pallets/flask",
    "https://github.com/django/django",
    "https://github.com/fastapi/fastapi"
]

for repo_url in repos:
    result = analyzer.analyze_repository(repo_url, max_commits=100)
    print(f"{result['repository']['name']}: {result['green_aware_percentage']:.1f}%")
```

### analyze_repository() Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `repo_url` | str | (required) | GitHub repository URL |
| `max_commits` | int | 1000 | Maximum commits to analyze |
| `since_date` | datetime | None | Start date filter |
| `to_date` | datetime | None | End date filter |

### Return Value

```python
{
    "repository": {
        "name": "flask",
        "url": "https://github.com/pallets/flask",
        "owner": "pallets",
        "clone_path": "/tmp/greenmining_repos/flask"
    },
    "total_commits": 200,
    "green_aware_count": 47,
    "green_aware_percentage": 23.5,
    "commits": [
        {
            "sha": "abc123...",
            "message": "Optimize template caching",
            "author": "developer",
            "date": "2024-03-15T10:30:00",
            "green_aware": True,
            "patterns": ["Cache Static Data"],
            "modified_files": 3,
            "insertions": 45,
            "deletions": 12,
            "dmm_unit_size": 0.85,
            "dmm_unit_complexity": 0.72,
            "dmm_unit_interfacing": 0.90
        },
        ...
    ],
    "pattern_distribution": {
        "Cache Static Data": 15,
        "Use Async Instead of Sync": 12,
        ...
    },
    "process_metrics": {
        "change_set": {"max": 25, "avg": 5.2},
        "code_churn": {"added": 5000, "removed": 2000},
        "contributors_count": 45
    }
}
```

---

## Complete Example

```python
#!/usr/bin/env python3
"""Analyze Flask repository for green patterns."""

from datetime import datetime
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

# Initialize analyzer
analyzer = LocalRepoAnalyzer(
    clone_path="/tmp/flask_analysis",
    cleanup_after=True
)

# Analyze repository
print("Analyzing Flask repository...")
result = analyzer.analyze_repository(
    repo_url="https://github.com/pallets/flask",
    max_commits=100,
    since_date=datetime(2024, 1, 1)
)

# Print summary
print(f"\n{'='*60}")
print("ANALYSIS RESULTS")
print(f"{'='*60}")
print(f"Repository: {result['repository']['name']}")
print(f"Total commits: {result['total_commits']}")
print(f"Green-aware: {result['green_aware_count']} ({result['green_aware_percentage']:.1f}%)")

# Top patterns
print(f"\nTop Patterns:")
for pattern, count in sorted(
    result['pattern_distribution'].items(), 
    key=lambda x: x[1], 
    reverse=True
)[:5]:
    print(f"  {pattern}: {count}")

# Sample green commits
print(f"\nSample Green Commits:")
green_commits = [c for c in result['commits'] if c['green_aware']]
for commit in green_commits[:5]:
    print(f"  🌱 {commit['message'][:60]}...")
    print(f"     Patterns: {commit['patterns']}")
```

**Output:**

```
Analyzing Flask repository...

============================================================
ANALYSIS RESULTS
============================================================
Repository: flask
Total commits: 100
Green-aware: 23 (23.0%)

Top Patterns:
  Cache Static Data: 8
  Use Async Instead of Sync: 5
  Lazy Loading: 4
  Compress Transmitted Data: 3
  Optimize Database Queries: 3

Sample Green Commits:
  🌱 Implement response caching for static assets...
     Patterns: ['Cache Static Data']
  🌱 Add async support for request handling...
     Patterns: ['Use Async Instead of Sync']
```

---

## Supported URL Formats

```python
# HTTPS (recommended)
"https://github.com/owner/repo"
"https://github.com/owner/repo.git"

# SSH
"git@github.com:owner/repo.git"

# With branch (coming soon)
"https://github.com/owner/repo/tree/branch-name"
```

---

## Commit Metrics

GreenMining extracts the following metrics for each commit:

### Basic Commit Metrics

| Metric | Description |
|--------|-------------|
| `modified_files` | Number of files changed |
| `insertions` | Lines added |
| `deletions` | Lines removed |
| `files` | List of modified file paths |

### DMM Metrics (Delta Maintainability Model)

Measures how a commit impacts code maintainability on a 0-1 scale (higher is better).

| Metric | Range | Description |
|--------|-------|-------------|
| `dmm_unit_size` | 0-1 | Unit size maintainability — proportion of changed code units that remain within acceptable size thresholds |
| `dmm_unit_complexity` | 0-1 | Cyclomatic complexity impact — proportion of changed code units with acceptable complexity |
| `dmm_unit_interfacing` | 0-1 | Interface complexity — proportion of changed code units with manageable parameter counts |

### Process Metrics

All 8 process metrics tracked per repository:

| Metric | Description |
|--------|-------------|
| `change_set` | Number of files changed per commit (max, avg) |
| `code_churn` | Lines added/removed over time |
| `contributors_count` | Unique contributors in the analysis period |
| `commits_count` | Total commits in the analysis period |
| `contributors_experience` | Average experience of contributors (commits to repo) |
| `history_complexity` | Normalized entropy of file change history |
| `hunks_count` | Number of contiguous changed blocks per file |
| `lines_count` | Total lines of code modified across all commits |

### Method-Level Metrics

When `method_level_analysis=True`, GreenMining uses Lizard to extract per-function metrics:

| Metric | Description |
|--------|-------------|
| `methods_count` | Number of methods analyzed in a commit |
| `total_nloc` | Total non-comment lines of code |
| `total_complexity` | Sum of cyclomatic complexity across all methods |
| `max_complexity` | Highest single-function complexity |

Each method entry includes:

| Field | Description |
|-------|-------------|
| `name` | Function/method name |
| `nloc` | Non-comment lines of code |
| `complexity` | Cyclomatic complexity |
| `token_count` | Number of tokens |
| `parameters` | Number of parameters |

---

## Configuration Options

Configure URL analysis via environment variables or Config:

```bash
# Environment variables
export CLONE_PATH=/custom/path
export CLEANUP_AFTER_ANALYSIS=false
export PROCESS_METRICS_ENABLED=true
export DMM_ENABLED=true
```

```python
# Python configuration
from greenmining.config import Config

config = Config()
print(config.CLONE_PATH)               # /tmp/greenmining_repos
print(config.CLEANUP_AFTER_ANALYSIS)   # True
print(config.PROCESS_METRICS_ENABLED)  # True
print(config.DMM_ENABLED)              # True
```

---

## Batch Analysis

Analyze multiple repositories efficiently:

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer
import json

repos = [
    "https://github.com/pallets/flask",
    "https://github.com/django/django",
    "https://github.com/fastapi/fastapi",
]

analyzer = LocalRepoAnalyzer(cleanup_after=True)
all_results = []

for url in repos:
    print(f"Analyzing {url}...")
    result = analyzer.analyze_repository(url, max_commits=100)
    all_results.append(result)
    print(f"  ✓ {result['green_aware_count']}/{result['total_commits']} green-aware")

# Save combined results
with open("batch_results.json", "w") as f:
    json.dump(all_results, f, indent=2, default=str)

# Summary
print(f"\nTotal repositories: {len(all_results)}")
total_commits = sum(r['total_commits'] for r in all_results)
total_green = sum(r['green_aware_count'] for r in all_results)
print(f"Total commits: {total_commits}")
print(f"Total green-aware: {total_green} ({total_green/total_commits*100:.1f}%)")
```

---

## Troubleshooting

### Clone Failures

```python
# Increase timeout
analyzer = LocalRepoAnalyzer(clone_timeout=300)  # 5 minutes

# Use SSH for private repos
result = analyzer.analyze_repository("git@github.com:org/private-repo.git")
```

### Large Repositories

```python
# Limit commits for large repos
result = analyzer.analyze_repository(
    repo_url="https://github.com/kubernetes/kubernetes",
    max_commits=500  # Limit for faster analysis
)
```

### Disk Space

```python
# Always cleanup
analyzer = LocalRepoAnalyzer(cleanup_after=True)

# Or manual cleanup
import shutil
shutil.rmtree("/tmp/greenmining_repos")
```

---

## Next Steps

- [Energy Measurement](energy.md) - Measure energy during analysis
- [Python API](api.md) - Full API reference
- [Configuration](../getting-started/configuration.md) - All settings
