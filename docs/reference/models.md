# Data Models Reference

Reference for GreenMining data models and structures.

---

## Core Models

### Repository

Represents a GitHub repository.

```python
from greenmining.models import Repository

repo = Repository(
    repo_id=12345,
    name="flask",
    full_name="pallets/flask",
    owner="pallets",
    url="https://github.com/pallets/flask",
    clone_url="https://github.com/pallets/flask.git",
    stars=65000,
    forks=16000,
    watchers=2500,
    open_issues=50,
    language="Python",
    last_updated="2024-01-15T10:00:00Z",
    created_at="2010-04-06T12:00:00Z",
    description="The Python micro framework for building web applications.",
    main_branch="main"
)
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `repo_id` | int | GitHub repository ID |
| `name` | str | Repository name |
| `full_name` | str | Full name (owner/repo) |
| `owner` | str | Repository owner |
| `url` | str | GitHub URL |
| `clone_url` | str | Git clone URL |
| `stars` | int | Star count |
| `forks` | int | Fork count |
| `watchers` | int | Watcher count |
| `open_issues` | int | Open issue count |
| `language` | str | Primary language |
| `last_updated` | str | Last update timestamp |
| `created_at` | str | Creation timestamp |
| `description` | str | Repository description |
| `main_branch` | str | Default branch name |

---

### Commit

Represents a Git commit.

```python
from greenmining.models import Commit

commit = Commit(
    sha="abc123def456789",
    message="Implement Redis caching for user sessions",
    author="developer",
    date="2024-01-15T10:30:00Z",
    repository="pallets/flask"
)
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `sha` | str | Commit SHA hash |
| `message` | str | Commit message |
| `author` | str | Author username |
| `date` | str | Commit timestamp (ISO 8601) |
| `repository` | str | Repository full name |

---

### AnalysisResult

Represents the analysis result for a commit.

```python
from greenmining.models import AnalysisResult

result = AnalysisResult(
    commit=commit,
    green_aware=True,
    patterns=["Cache Static Data"],
    confidence=0.85
)
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `commit` | Commit | The analyzed commit |
| `green_aware` | bool | Whether commit is green-aware |
| `patterns` | list[str] | Matched pattern names |
| `confidence` | float | Detection confidence (0-1) |

---

## Analysis Output Structures

### Commit Analysis Dictionary

When commits are analyzed, they're returned as dictionaries:

```python
{
    "sha": "abc123def456789",
    "message": "Implement Redis caching for user sessions",
    "author": "developer",
    "date": "2024-01-15T10:30:00Z",
    "repository": "pallets/flask",
    "green_aware": True,
    "patterns": ["Cache Static Data"],
    "category": "caching",
    "keywords_matched": ["redis", "caching"],
    "confidence": 0.85,
    
    # If diff analysis enabled
    "diff_patterns": ["caching"],
    "files_modified": 3,
    
    # If process metrics enabled
    "insertions": 45,
    "deletions": 12,
    "dmm_unit_size": 0.85,
    "dmm_unit_complexity": 0.72,
    "dmm_unit_interfacing": 0.90
}
```

---

### Aggregated Statistics Structure

Output from `DataAggregator.aggregate()`:

```python
{
    "summary": {
        "total_commits": 5000,
        "green_aware_count": 1250,
        "green_aware_percentage": 25.0,
        "total_repos": 50,
        "repos_with_green_commits": 42,
        "analysis_date": "2024-01-15T10:00:00Z"
    },
    
    "pattern_distribution": {
        "Cache Static Data": 320,
        "Use Async Instead of Sync": 180,
        "Compress Transmitted Data": 150,
        "Lazy Loading": 120,
        "Optimize Database Queries": 95
    },
    
    "category_distribution": {
        "cloud": 450,
        "caching": 320,
        "async": 210,
        "web": 180,
        "database": 95
    },
    
    "per_repo_stats": [
        {
            "repository": "pallets/flask",
            "total_commits": 200,
            "green_aware_count": 47,
            "green_aware_percentage": 23.5,
            "top_patterns": ["Cache Static Data", "Lazy Loading"]
        }
    ],
    
    "per_language_stats": {
        "Python": {
            "total_commits": 2000,
            "green_aware_count": 520,
            "green_aware_percentage": 26.0
        }
    },
    
    # If enable_temporal=True
    "temporal_analysis": {
        "periods": [
            {
                "period": "2024-Q1",
                "commit_count": 500,
                "green_count": 125,
                "green_awareness_rate": 0.25
            }
        ],
        "overall_trend": {
            "direction": "increasing",
            "significant": True
        }
    },
    
    # If enable_stats=True
    "statistics": {
        "pattern_correlations": {
            "top_positive_correlations": [
                {
                    "pattern1": "caching",
                    "pattern2": "performance",
                    "correlation": 0.75
                }
            ]
        },
        "effect_size": {
            "green_vs_nongreen_patterns": {
                "cohens_d": 0.65,
                "magnitude": "medium"
            }
        },
        "descriptive": {
            "patterns_per_commit": {
                "mean": 2.3,
                "median": 2.0,
                "std": 1.1
            }
        }
    }
}
```

---

### URL Analysis Result Structure

Output from `LocalRepoAnalyzer.analyze_repository()`:

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
            
            # Process metrics
            "modified_files": 3,
            "insertions": 45,
            "deletions": 12,
            "files": ["app.py", "cache.py", "config.py"],
            
            # DMM metrics
            "dmm_unit_size": 0.85,
            "dmm_unit_complexity": 0.72,
            "dmm_unit_interfacing": 0.90
        }
    ],
    
    "pattern_distribution": {
        "Cache Static Data": 15,
        "Use Async Instead of Sync": 12,
        "Lazy Loading": 8
    },
    
    "process_metrics": {
        "change_set": {
            "max": 25,
            "avg": 5.2
        },
        "code_churn": {
            "added": 5000,
            "removed": 2000
        },
        "contributors_count": 45,
        "commits_count": 200
    }
}
```

---

## Energy Metrics Structures

### EnergyMetrics

```python
from greenmining.energy.base import EnergyMetrics

@dataclass
class EnergyMetrics:
    energy_joules: float       # Total energy consumed
    duration_seconds: float    # Measurement duration
    average_power_watts: float # Average power draw
    start_time: datetime       # Start timestamp
    end_time: datetime         # End timestamp
    
    # CodeCarbon specific
    energy_kwh: float = 0.0    # Energy in kWh
    emissions_kg: float = 0.0  # CO2 emissions
```

### CommitEnergyProfile

```python
from greenmining.energy.base import CommitEnergyProfile

@dataclass
class CommitEnergyProfile:
    commit_sha: str            # Commit identifier
    energy_joules: float       # Energy for this commit
    duration_seconds: float    # Analysis duration
    patterns_detected: list    # Patterns found
    files_analyzed: int        # Files in commit
```

---

## Pattern Structure

GSF patterns are stored as dictionaries:

```python
{
    "cache_static_data": {
        "name": "Cache Static Data",
        "category": "cloud",
        "keywords": ["cache", "caching", "static", "cdn", "redis", "memcache"],
        "description": "Cache static content to reduce server load and network transfers",
        "sci_impact": "Reduces energy by minimizing redundant compute and network operations"
    }
}
```

#### Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Human-readable pattern name |
| `category` | str | Pattern category |
| `keywords` | list[str] | Detection keywords |
| `description` | str | Pattern description |
| `sci_impact` | str | Impact on software carbon intensity |

---

## Working with Models

### Serialization

```python
import json

# Convert to JSON
result_json = json.dumps(analysis_result, default=str)

# Load from JSON
with open("results.json") as f:
    results = json.load(f)
```

### Filtering Results

```python
# Get only green-aware commits
green_commits = [c for c in commits if c["green_aware"]]

# Group by pattern
from collections import defaultdict
by_pattern = defaultdict(list)
for commit in green_commits:
    for pattern in commit["patterns"]:
        by_pattern[pattern].append(commit)

# Get top patterns
top_patterns = sorted(
    by_pattern.items(), 
    key=lambda x: len(x[1]), 
    reverse=True
)[:10]
```

### Aggregating Custom Metrics

```python
import statistics

# Calculate custom statistics
green_counts = [r["green_aware_count"] for r in per_repo_stats]
avg_green = statistics.mean(green_counts)
median_green = statistics.median(green_counts)
std_green = statistics.stdev(green_counts) if len(green_counts) > 1 else 0
```

---

## Next Steps

- [Python API](../user-guide/api.md) - Working with models
- [GSF Patterns](patterns.md) - Pattern reference
- [Configuration](../getting-started/configuration.md) - All options
