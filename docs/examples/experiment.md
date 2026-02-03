# Experiment: Unified Repository Analysis Pipeline

This page describes the reference experiment included with GreenMining. The Jupyter notebook
(`experiment/beta/experiment.ipynb`) demonstrates every feature of the library in a single,
end-to-end pipeline applied to 15 repositories.

## Overview

- **5 cloud repositories** found via GraphQL search
- **5 S2-group research repositories** manually selected (SAF-Toolkit, UPISAS, experiment-runner, robot-runner, android-runner)
- **Total: 10 repositories** — all analyzed with the same pipeline and ALL features enabled
- **Commits per repository:** 50 (max)
- **Min stars:** 5
- **Languages:** 21 top programming languages
- **Date range:** 2020-01-01 to 2026-12-31

The experiment follows a 16-step pipeline:

| Step | Purpose | Library Features Used |
|------|---------|----------------------|
| 1-2 | Setup & Configuration | `greenmining` package, `GSF_PATTERNS`, `GREEN_KEYWORDS` |
| 3-4 | Data Gathering | `fetch_repositories`, `analyze_repositories` |
| 5-12 | Analysis | All analyzers, energy measurement |
| 13-15 | Visualization & Export | matplotlib, Plotly, JSON/CSV export |

---

## Step 1: Import Libraries

Install and import all GreenMining modules:

```python
%pip install greenmining[energy] --upgrade --quiet

import greenmining
from greenmining import (
    fetch_repositories,
    analyze_repositories,
    GSF_PATTERNS,
    GREEN_KEYWORDS,
    is_green_aware,
    get_pattern_by_keywords,
)
from greenmining.analyzers import (
    StatisticalAnalyzer,
    TemporalAnalyzer,
    CodeDiffAnalyzer,
    MetricsPowerCorrelator,
)
from greenmining.energy import get_energy_meter, CPUEnergyMeter
```

```
GreenMining version: 1.2.x
GSF Patterns: 124
Green Keywords: 332
```

---

## Step 2: Configuration

Shared parameters used across the entire pipeline:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `MAX_COMMITS` | 50 | Commits analyzed per repository |
| `MIN_STARS` | 5 | Minimum GitHub stars for search |
| `PARALLEL_WORKERS` | 5 | Concurrent repository analysis |
| `LANGUAGES` | 21 | Top programming languages |
| `CREATED_AFTER` | `2020-01-01` | Repository creation lower bound |
| `CREATED_BEFORE` | `2026-12-31` | Repository creation upper bound |
| `PUSHED_AFTER` | `2020-01-01` | Recent activity filter |
| `COMMIT_DATE_FROM` | `2020-01-01` | Commit analysis start date |
| `COMMIT_DATE_TO` | `2026-12-31` | Commit analysis end date |

The GitHub token is loaded from the environment or a `.env` file.

---

## Step 3: Search Repositories

Uses `fetch_repositories()` with the **GraphQL API v4** to find 10 mobile app repositories:

```python
search_repos = fetch_repositories(
    github_token=GITHUB_TOKEN,
    max_repos=10,
    min_stars=MIN_STARS,
    languages=LANGUAGES,
    keywords='mobile app',
    created_after=CREATED_AFTER,
    created_before=CREATED_BEFORE,
    pushed_after=PUSHED_AFTER,
)
```

```
Found 10 mobile app repositories:
   1. example/repo-1 (1000 stars, TypeScript)
   2. example/repo-2 (500 stars, Dart)
   ...
```

---

## Step 4: Analyze Repositories

Combines the 10 searched repositories with 5 manually selected S2-group repositories,
then runs the full analysis pipeline on all of them:

```python
# 5 manually selected repositories
manual_urls = [
    'https://github.com/S2-group/green-lab',
    'https://github.com/S2-group/UPISAS',
    'https://github.com/S2-group/experiment-runner',
    'https://github.com/S2-group/robot-runner',
    'https://github.com/S2-group/android-runner',
]

# Combine all URLs
all_urls = search_urls + manual_urls  # Total: 15 repositories

# Analyze ALL repositories with ALL features
raw_results = analyze_repositories(
    urls=all_urls,
    max_commits=MAX_COMMITS,
    parallel_workers=PARALLEL_WORKERS,
    output_format='dict',
    energy_tracking=True,
    energy_backend='auto',
    method_level_analysis=True,
    include_source_code=True,
    github_token=GITHUB_TOKEN,
    since_date=COMMIT_DATE_FROM,
    to_date=COMMIT_DATE_TO,
)
results = [r.to_dict() for r in raw_results]
```

**Library features applied per repository:**

- GSF pattern detection (124 patterns, 15 categories, 332 keywords)
- Process metrics (DMM unit size, complexity, interfacing)
- Method-level analysis (per-function complexity via Lizard)
- Source code capture (before/after for each modified file)
- Energy measurement (auto-detected backend)

---

## Step 5: Results Overview

Summary of the analysis across all repositories:

```
======================================================================
ANALYSIS SUMMARY
======================================================================
Repositories analyzed: 15
Total commits: ~700
Green-aware commits: ~200
Overall green rate: ~30%
```

---

## Step 6: GSF Pattern Analysis

Counts pattern frequency across all commits and groups patterns by category:

```python
# Pattern frequency across all commits
pattern_counts = {}
for commit in all_commits:
    for pattern in commit.get('gsf_patterns_matched', []):
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
```

```
Unique patterns detected: 46

Top 10 GSF Patterns:
Pattern                                  Count    % of Commits
-----------------------------------------------------------------
Keep Request Counts Low                  17       9.1%
Containerize Your Workload               13       7.0%
Use Compiled Languages                   13       7.0%
...

GSF Categories (15):
  ai, async, caching, cloud, code, data, database,
  general, infrastructure, microservices, monitoring,
  network, networking, resource, web
```

---

## Step 7: Process Metrics

Examines DMM scores, structural complexity, and method-level data:

| Metric | Description |
|--------|-------------|
| `dmm_unit_size` | Delta Maintainability Model -- size (0-1) |
| `dmm_unit_complexity` | Delta Maintainability Model -- complexity (0-1) |
| `dmm_unit_interfacing` | Delta Maintainability Model -- interfacing (0-1) |
| `total_nloc` | Total non-comment lines of code |
| `total_complexity` | Cyclomatic complexity sum |
| `max_complexity` | Highest single-function complexity |
| `methods_count` | Number of methods analyzed |

---

## Step 8: Statistical Analysis

Applies statistical methods to the combined dataset:

```python
stat_analyzer = StatisticalAnalyzer()
stat_analyzer.analyze_pattern_correlations(commits_df)
stat_analyzer.temporal_trend_analysis(commits_df)
stat_analyzer.effect_size_analysis(green_cx, non_green_cx)
```

| Method | Output |
|--------|--------|
| `analyze_pattern_correlations()` | Significant co-occurrence pairs |
| `temporal_trend_analysis()` | Trend direction, significance, correlation |
| `effect_size_analysis()` | Cohen's d, magnitude, mean difference |

---

## Step 9: Temporal Analysis

Groups commits by quarter and tracks green awareness evolution:

```python
temporal = TemporalAnalyzer(granularity='quarter')
temporal_results = temporal.analyze_trends(all_commits, analysis_results_fmt)
```

Output includes period-by-period green commit rates, unique pattern counts,
overall trend direction, and peak period identification.

---

## Step 10: Code Diff Pattern Signatures

Inspects the green pattern categories that `CodeDiffAnalyzer` detects in code diffs:

```python
diff_analyzer = CodeDiffAnalyzer()
print(diff_analyzer.PATTERN_SIGNATURES)
```

```
Code Diff Pattern Signatures: 15 types
  caching, resource_optimization, database_optimization,
  async_processing, lazy_loading, serverless_computing,
  cdn_edge, compression, model_optimization,
  efficient_protocols, container_optimization, green_regions,
  auto_scaling, code_splitting, green_ml_training
```

---

## Step 11: Energy Measurement

Demonstrates multiple energy measurement approaches:

| Backend | Platform | What It Measures |
|---------|----------|------------------|
| RAPL | Linux (Intel/AMD) | Hardware energy counters (Joules) |
| CPU Meter | Universal | CPU utilization + TDP estimate (Joules) |
| tracemalloc | Universal | Peak memory allocation (bytes) |
| CodeCarbon | Cross-platform | CO2 emissions (kg CO2eq) |

```python
# RAPL (Linux Intel/AMD)
from greenmining.energy import RAPLEnergyMeter
rapl = RAPLEnergyMeter()
result, energy = rapl.measure(sample_workload)

# CPU Meter (universal)
meter = CPUEnergyMeter()
result, energy = meter.measure(sample_workload)

# CodeCarbon
from codecarbon import EmissionsTracker
tracker = EmissionsTracker()
tracker.start()
# ... workload ...
emissions = tracker.stop()
```

---

## Step 12: Metrics-to-Power Correlation

Correlates code metrics with energy consumption:

```python
correlator = MetricsPowerCorrelator(significance_level=0.05)
correlator.fit(metric_names, metrics_values, power_measurements)
summary = correlator.summary()
```

Computes Pearson and Spearman coefficients with significance testing,
plus feature importance ranking across all metrics.

---

## Step 13: Visualization (matplotlib)

Static 2x2 chart grid:

1. Green commit rate per repository (horizontal bar)
2. Top 10 GSF patterns (horizontal bar)
3. Total vs green commit breakdown (grouped bar)
4. Complexity distribution (histogram)

Saved to `data/analysis_plots.png`.

---

## Step 14: Interactive Visualization (Plotly)

Interactive charts:

- **Sunburst:** Repository → Green/Non-Green → Pattern
- **Scatter:** Complexity vs Lines of Code, colored by green awareness

---

## Step 15: Export Results

Exports the analysis in multiple formats:

### Output Structure

```
data/
├── repositories/           # Individual repo analyses (full data)
│   ├── repo-name-1.json
│   ├── repo-name-2.json
│   └── ...
├── analysis_summary.json   # All repos, no source code (~2-5 MB)
├── analysis_results.csv    # Flattened commit-level (~200 KB)
└── statistics.json         # High-level overview (~10 KB)
```

### File Descriptions

| File | Size | Content |
|------|------|---------|
| `repositories/*.json` | Large | Full analysis per repo (includes source code) |
| `analysis_summary.json` | Medium | All repos without `source_changes` and `methods` |
| `analysis_results.csv` | Small | Flattened commit-level data for spreadsheets |
| `statistics.json` | Tiny | Overall stats, top patterns, repo summary |

---

## Feature Coverage

The experiment applies every library feature to every repository:

| Feature | Module | Applied |
|---------|--------|---------|
| GSF Pattern Detection (124 patterns, 15 categories) | `greenmining` | ✅ |
| Process Metrics (DMM size, complexity, interfacing) | `greenmining` | ✅ |
| Method-Level Analysis (per-function complexity) | `greenmining` | ✅ |
| Source Code Capture (before/after) | `greenmining` | ✅ |
| Energy Measurement (RAPL + CPU Meter) | `greenmining.energy` | ✅ |
| Memory Profiling (tracemalloc) | `tracemalloc` | ✅ |
| CO2 Emissions (CodeCarbon) | `codecarbon` | ✅ |
| Statistical Analysis (correlations, effect sizes) | `greenmining.analyzers` | ✅ |
| Temporal Analysis (quarterly trends) | `greenmining.analyzers` | ✅ |
| Code Diff Pattern Signatures | `greenmining.analyzers` | ✅ |
| Metrics-to-Power Correlation (Pearson/Spearman) | `greenmining.analyzers` | ✅ |
| Visualization (matplotlib + Plotly) | External | ✅ |
| Export (JSON, CSV, DataFrame) | Built-in | ✅ |

---

## Running the Experiment

```bash
# Install the library
pip install greenmining[energy]

# Set your GitHub token
export GITHUB_TOKEN=ghp_your_token_here

# Open the notebook
jupyter notebook experiment/beta/experiment.ipynb
```

Run all cells sequentially. The data gathering steps require a valid GitHub token
and internet access.
