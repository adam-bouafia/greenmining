# Python API Reference

Use GreenMining programmatically in your Python scripts.

---

## Quick Import

```python
from greenmining import (
    GSF_PATTERNS,        # Dict of 122 GSF patterns
    GREEN_KEYWORDS,      # List of 321 green keywords
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

Dictionary containing all 122 Green Software Foundation patterns.

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
print(f"Total patterns: {len(GSF_PATTERNS)}")  # 122

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

List of 321 keywords indicating green software practices.

```python
from greenmining import GREEN_KEYWORDS

print(f"Total keywords: {len(GREEN_KEYWORDS)}")  # 321

# Sample keywords
print(GREEN_KEYWORDS[:10])
# ['energy', 'power', 'carbon', 'emission', 'footprint', 
#  'sustainability', 'sustainable', 'green', 'efficient', 'efficiency']
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
    config=None,                  # Config object
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

Analyze repositories directly from GitHub URLs using PyDriller.

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer(
    clone_path="/tmp/greenmining_repos",  # Clone directory
    cleanup_after=True                     # Delete after analysis
)
```

**Methods:**

```python
# Analyze single repository
result = analyzer.analyze_repository(
    repo_url="https://github.com/owner/repo",
    max_commits=1000,
    since_date=datetime(2024, 1, 1),
    to_date=datetime(2024, 12, 31)
)
```

**Example:**

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer
from datetime import datetime

analyzer = LocalRepoAnalyzer(
    clone_path="/tmp/analysis",
    cleanup_after=True
)

result = analyzer.analyze_repository(
    repo_url="https://github.com/pallets/flask",
    max_commits=100
)

print(f"Repository: {result['repository']['name']}")
print(f"Commits analyzed: {result['total_commits']}")
print(f"Green-aware: {result['green_aware_count']}")

# Access individual commits
for commit in result['commits'][:5]:
    if commit['green_aware']:
        print(f"  🌱 {commit['message'][:50]}...")
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

# PyDriller options
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
- [GSF Patterns Reference](../reference/patterns.md) - All 122 patterns
