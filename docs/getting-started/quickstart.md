# Quick Start

Get up and running with GreenMining in 5 minutes.

---

## Prerequisites

- Python 3.9+
- GitHub token (for fetching repositories)
- GreenMining installed (`pip install greenmining`)

---

## Option 1: Analyze a Repository by URL

Analyze any public GitHub repository directly:

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer()
result = analyzer.analyze_repository(
    "https://github.com/pallets/flask",
    max_commits=100
)

print(f"Repository: {result['repository']['name']}")
print(f"Total commits: {result['total_commits']}")
print(f"Green-aware: {result['green_aware_count']} ({result['green_aware_percentage']:.1f}%)")

print("\nTop Patterns:")
for pattern, count in sorted(
    result['pattern_distribution'].items(),
    key=lambda x: x[1],
    reverse=True
)[:5]:
    print(f"  - {pattern}: {count}")
```

**Output:**

```
Repository: flask
Total commits: 100
Green-aware: 23 (23.0%)

Top Patterns:
  - Cache Static Data: 8
  - Use Async Instead of Sync: 5
  - Lazy Loading: 4
```

---

## Option 2: Full Pipeline (Comprehensive)

Run the complete analysis pipeline programmatically:

```python
import os
from greenmining.services import (
    GitHubFetcher,
    CommitExtractor,
    DataAnalyzer,
    DataAggregator,
)

# Set your GitHub token
github_token = os.environ.get("GITHUB_TOKEN")

# 1. Fetch repositories
fetcher = GitHubFetcher(token=github_token, max_repos=5, min_stars=500)
repos = fetcher.search_repositories()

# 2. Extract commits
extractor = CommitExtractor(max_commits=50)
commits = extractor.extract_from_repositories(repos)

# 3. Analyze commits
analyzer = DataAnalyzer()
results = analyzer.analyze_commits(commits)

# 4. Aggregate statistics
aggregator = DataAggregator(enable_stats=True, enable_temporal=True)
stats = aggregator.aggregate(results, repos)

# Print results
print(f"Repositories analyzed: {len(repos)}")
print(f"Total commits: {len(commits)}")
print(f"Green-aware: {stats['green_aware_percentage']:.1f}%")
```

---

## Option 3: Quick Pattern Detection

Use GreenMining programmatically:

```python
from greenmining import GSF_PATTERNS, is_green_aware, get_pattern_by_keywords

# Check pattern count
print(f"Loaded {len(GSF_PATTERNS)} GSF patterns")
# Output: Loaded 124 GSF patterns

# Test green awareness detection
messages = [
    "Optimize Redis caching for better performance",
    "Fix typo in README",
    "Enable gzip compression for API responses",
    "Update dependencies to latest versions",
]

for msg in messages:
    is_green = is_green_aware(msg)
    patterns = get_pattern_by_keywords(msg) if is_green else []
    status = "🌱" if is_green else "  "
    print(f"{status} {msg[:50]}")
    if patterns:
        print(f"   → Patterns: {patterns}")
```

**Output:**

```
🌱 Optimize Redis caching for better performance
   → Patterns: ['Cache Static Data']
   Fix typo in README
🌱 Enable gzip compression for API responses
   → Patterns: ['Compress Transmitted Data', 'Enable Text Compression']
   Update dependencies to latest versions
```

---

## Output Files

When running the pipeline, outputs are saved to the `data/` directory:

| File | Description |
|------|-------------|
| `repositories.json` | Fetched repository metadata |
| `commits.json` | Extracted commit data |
| `analysis_results.json` | Pattern detection results |
| `aggregated_statistics.json` | Summary statistics |
| `aggregated_data.json` | Full aggregated data |

---

## Quick Test Script

Create `test_greenmining.py`:

```python
#!/usr/bin/env python3
"""Quick test of GreenMining functionality."""

from greenmining import GSF_PATTERNS, GREEN_KEYWORDS, is_green_aware, get_pattern_by_keywords

# Test 1: Check patterns loaded
print(f"✓ Loaded {len(GSF_PATTERNS)} GSF patterns")
print(f"✓ Loaded {len(GREEN_KEYWORDS)} green keywords")

# Test 2: Get categories
categories = set(p["category"] for p in GSF_PATTERNS.values())
print(f"✓ Categories: {', '.join(sorted(categories))}")

# Test 3: Pattern detection
test_msg = "Implement Redis caching to reduce database load"
is_green = is_green_aware(test_msg)
patterns = get_pattern_by_keywords(test_msg)

print(f"✓ Test message: '{test_msg}'")
print(f"  Green-aware: {is_green}")
print(f"  Patterns: {patterns}")

print("\n✅ All tests passed!")
```

Run it:

```bash
python test_greenmining.py
```

---

## Next Steps

- [Configuration](configuration.md) - Customize settings
- [Python API](../user-guide/api.md) - Programmatic usage
- [GSF Patterns](../reference/patterns.md) - All 124 patterns
- [URL Analysis](../user-guide/url-analysis.md) - Analyze by URL
