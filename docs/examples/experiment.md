# Experiment: Unified Repository Analysis Pipeline

This page describes the reference experiment included with GreenMining. The Jupyter notebook
(`experiment/beta/experiment.ipynb`) demonstrates every feature of the library in a single,
end-to-end pipeline applied to 13 repositories.

## Overview

The experiment follows a four-part structure:

| Part | Purpose | Library Features Used |
|------|---------|----------------------|
| **A: Setup** | Install, import, configure | `greenmining` package, `GSF_PATTERNS`, `GREEN_KEYWORDS` |
| **B: Data Gathering** | Fetch and analyze repositories | `fetch_repositories`, `analyze_repositories` |
| **C: Unified Analysis** | Apply every analyzer to the combined dataset | All analyzers, energy, visualization, export |
| **D: Summary** | Feature coverage table and output files | -- |

---

## Part A: Setup

### Step 1 -- Install

```python
!pip install greenmining[energy] --upgrade --quiet
```

The `[energy]` extra installs optional dependencies for energy measurement (CodeCarbon).

### Step 2 -- Imports

All modules are imported from the library:

```python
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
    PowerRegressionDetector,
    MetricsPowerCorrelator,
    VersionPowerAnalyzer,
)
from greenmining.energy import get_energy_meter, CPUEnergyMeter
import tracemalloc
```

### Step 3 -- Configuration

Shared parameters used across the entire pipeline:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `MAX_COMMITS` | 20 | Commits analyzed per repository |
| `MIN_STARS` | 3 | Minimum GitHub stars for search |
| `PARALLEL_WORKERS` | 2 | Concurrent repository analysis |
| `LANGUAGES` | 20 | Top programming languages |
| `CREATED_AFTER` | `2020-01-01` | Repository creation lower bound |
| `CREATED_BEFORE` | `2023-12-31` | Repository creation upper bound |
| `PUSHED_AFTER` | `2023-01-01` | Recent activity filter |
| `COMMIT_DATE_FROM` | `2023-01-01` | Commit analysis start date |
| `COMMIT_DATE_TO` | `2025-12-31` | Commit analysis end date |

The GitHub token is loaded from the environment or a `.env` file.

---

## Part B: Data Gathering

### Step 4 -- Search Blockchain Repositories

Uses `fetch_repositories()` with the **GraphQL API v4** to find 10 blockchain repositories:

```python
search_repos = fetch_repositories(
    github_token=GITHUB_TOKEN,
    max_repos=10,
    min_stars=MIN_STARS,
    languages=LANGUAGES,
    keywords="blockchain",
    created_after=CREATED_AFTER,
    created_before=CREATED_BEFORE,
    pushed_after=PUSHED_AFTER,
)
```

**Library feature:** `greenmining.fetch_repositories` wraps `GitHubGraphQLFetcher.search_repositories`.
When more than 5 languages are provided, the language filter is skipped to stay within
GitHub query complexity limits. Date filters (`created_after`, `created_before`, `pushed_after`)
narrow the search to repositories within specific time windows.

### Step 5 -- Analyze All 13 Repositories

Combines the 10 searched repositories with 3 manually selected ones (Flask, Requests, FastAPI),
then runs the full analysis pipeline on all of them at once:

```python
raw_results = analyze_repositories(
    urls=all_urls,
    max_commits=MAX_COMMITS,
    parallel_workers=PARALLEL_WORKERS,
    output_format="dict",
    energy_tracking=True,
    energy_backend="auto",
    method_level_analysis=True,
    include_source_code=True,
    github_token=GITHUB_TOKEN,
    since_date=COMMIT_DATE_FROM,
    to_date=COMMIT_DATE_TO,
)
results = [r.to_dict() for r in raw_results]
```

`analyze_repositories()` returns a list of `RepositoryAnalysis` dataclass objects. These are
converted to dictionaries with `.to_dict()` for downstream processing.

**Library features applied per repository:**

- GSF pattern detection (122 patterns, 15 categories, 321 keywords)
- Process metrics (DMM unit size, complexity, interfacing)
- Method-level analysis (per-function complexity via Lizard)
- Source code capture (before/after for each modified file)
- Energy measurement (auto-detected backend)
- Date-bounded commit analysis (`since_date` / `to_date`)

### Step 6 -- Results Overview

Prints a summary table and builds a flat `all_commits` list used by every subsequent analysis step.

---

## Part C: Unified Analysis

Every analyzer operates on the combined dataset of all 13 repositories.

### Step 7 -- GSF Pattern Analysis

Counts pattern frequency across all commits and groups patterns by category.

**Library features:** `GSF_PATTERNS` dictionary (122 patterns), category grouping.

### Step 8 -- Green Awareness Detection

Demonstrates `is_green_aware()` on sample commit messages and `get_pattern_by_keywords()` for
pattern lookup.

**Library features:** `greenmining.is_green_aware`, `greenmining.get_pattern_by_keywords`.

### Step 9 -- Process Metrics

Inspects DMM scores, structural complexity, and method-level data collected during analysis.

**Library features:** Process metrics from `analyze_repositories` with `method_level_analysis=True`.

| Metric | Description |
|--------|-------------|
| `dmm_unit_size` | Delta Maintainability Model -- size (0-1) |
| `dmm_unit_complexity` | Delta Maintainability Model -- complexity (0-1) |
| `dmm_unit_interfacing` | Delta Maintainability Model -- interfacing (0-1) |
| `total_nloc` | Total non-comment lines of code |
| `total_complexity` | Cyclomatic complexity sum |
| `max_complexity` | Highest single-function complexity |
| `methods_count` | Number of methods analyzed |

### Step 10 -- Statistical Analysis

Applies three statistical methods to the combined dataset:

```python
stat_analyzer = StatisticalAnalyzer()
stat_analyzer.analyze_pattern_correlations(commits_df)
stat_analyzer.temporal_trend_analysis(commits_df)
stat_analyzer.effect_size_analysis(green_cx, non_green_cx)
```

**Library feature:** `greenmining.analyzers.StatisticalAnalyzer`

| Method | Output |
|--------|--------|
| `analyze_pattern_correlations()` | Significant co-occurrence pairs |
| `temporal_trend_analysis()` | Trend direction, significance, correlation |
| `effect_size_analysis()` | Cohen's d, magnitude, mean difference |

### Step 11 -- Temporal Analysis

Groups commits by quarter and tracks green awareness evolution over time:

```python
temporal = TemporalAnalyzer(granularity="quarter")
temporal_results = temporal.analyze_trends(all_commits, analysis_results_fmt)
```

**Library feature:** `greenmining.analyzers.TemporalAnalyzer`

Output includes period-by-period green commit rates, unique pattern counts, overall trend
direction, and peak period identification.

### Step 12 -- Code Diff Pattern Signatures

Inspects the 15+ green pattern categories that `CodeDiffAnalyzer` detects directly in code diffs:

```python
diff_analyzer = CodeDiffAnalyzer()
print(diff_analyzer.PATTERN_SIGNATURES)
```

**Library feature:** `greenmining.analyzers.CodeDiffAnalyzer`

Pattern signatures include caching, lazy loading, compression, connection pooling,
batch processing, async I/O, and more.

### Step 13 -- Energy Measurement

Demonstrates all four energy measurement approaches:

**RAPL (Running Average Power Limit):**

```python
from greenmining.energy import RAPLEnergyMeter
rapl = RAPLEnergyMeter()
result, energy = rapl.measure(workload_function)
```

**CPU Meter (universal fallback):**

```python
meter = CPUEnergyMeter()
result, energy = meter.measure(workload_function)
```

**Memory Profiling (tracemalloc):**

```python
tracemalloc.start()
# ... workload ...
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
```

**CO2 Emissions (CodeCarbon):**

```python
from codecarbon import EmissionsTracker
tracker = EmissionsTracker(project_name="greenmining-experiment")
tracker.start()
# ... workload ...
emissions = tracker.stop()
```

| Backend | Platform | What It Measures |
|---------|----------|------------------|
| RAPL | Linux (Intel/AMD) | Hardware energy counters (Joules) |
| CPU Meter | Universal | CPU utilization + TDP estimate (Joules) |
| tracemalloc | Universal | Peak memory allocation (bytes) |
| CodeCarbon | Cross-platform | CO2 emissions (kg CO2eq) |

### Step 14 -- Power Regression Detection

Identifies commits that caused energy consumption increases:

```python
detector = PowerRegressionDetector(
    test_command="python -c 'sum(range(100000))'",
    energy_backend="cpu_meter",
    threshold_percent=5.0,
    iterations=3,
)
regressions = detector.detect(
    repo_path="./my-repo",
    baseline_commit="HEAD~10",
    target_commit="HEAD",
)
```

**Library feature:** `greenmining.analyzers.PowerRegressionDetector`

Runs the test command at each commit, measures energy, and flags regressions above the threshold.

### Step 15 -- Metrics-to-Power Correlation

Correlates code metrics (complexity, NLOC, churn) with energy consumption:

```python
correlator = MetricsPowerCorrelator(significance_level=0.05)
correlator.fit(metric_names, metrics_values, power_measurements)
summary = correlator.summary()
```

**Library feature:** `greenmining.analyzers.MetricsPowerCorrelator`

Computes Pearson and Spearman coefficients with significance testing, plus feature importance
ranking across all metrics.

### Step 16 -- Version Power Analysis

Compares energy consumption across software versions:

```python
version_analyzer = VersionPowerAnalyzer(
    test_command="python -c 'sum(range(100000))'",
    energy_backend="cpu_meter",
    iterations=5,
)
report = version_analyzer.analyze_versions(
    repo_path="./my-repo",
    versions=["v1.0", "v2.0", "v3.0"],
)
```

**Library feature:** `greenmining.analyzers.VersionPowerAnalyzer`

Reports per-version power consumption, overall trend, most/least efficient versions,
and total change percentage.

### Step 17 -- Visualization (matplotlib)

Static 2x2 chart grid:

1. Green commit rate per repository (horizontal bar)
2. Top 10 GSF patterns (horizontal bar)
3. Total vs green commit breakdown (grouped bar)
4. Complexity distribution (histogram)

Saved to `data/analysis_plots.png`.

### Step 18 -- Interactive Visualization (Plotly)

Interactive charts:

- **Sunburst:** Repository > Green/Non-Green > Pattern
- **Scatter:** Complexity vs Lines of Code, colored by green awareness

### Step 19 -- Export Results

Exports the combined dataset in three formats:

| Format | File | Content |
|--------|------|---------|
| JSON | `data/analysis_results.json` | Full analysis data (all fields) |
| CSV | `data/analysis_results.csv` | Flattened commit-level rows |
| DataFrame | In-memory | pandas DataFrame for further analysis |

---

## Part D: Summary

### Feature Coverage

The experiment applies every library feature to every repository equally:

| Feature | Module | Applied |
|---------|--------|---------|
| GSF Pattern Detection (122 patterns, 15 categories) | `greenmining` | Yes |
| Process Metrics (DMM size, complexity, interfacing) | `greenmining` | Yes |
| Method-Level Analysis (per-function complexity) | `greenmining` | Yes |
| Source Code Capture (before/after) | `greenmining` | Yes |
| Energy Measurement (RAPL + CPU Meter) | `greenmining.energy` | Yes |
| Memory Profiling (tracemalloc) | `tracemalloc` | Yes |
| CO2 Emissions (CodeCarbon) | `codecarbon` | Yes |
| Statistical Analysis (correlations, effect sizes) | `greenmining.analyzers` | Yes |
| Temporal Analysis (quarterly trends) | `greenmining.analyzers` | Yes |
| Code Diff Pattern Signatures | `greenmining.analyzers` | Yes |
| Power Regression Detection | `greenmining.analyzers` | Demonstrated |
| Metrics-to-Power Correlation (Pearson/Spearman) | `greenmining.analyzers` | Yes |
| Version Power Comparison | `greenmining.analyzers` | Demonstrated |
| Visualization (matplotlib + Plotly) | External | Yes |
| Export (JSON, CSV, DataFrame) | Built-in | Yes |

### Output Files

| File | Description |
|------|-------------|
| `data/analysis_results.json` | Full analysis data |
| `data/analysis_results.csv` | Flattened commit-level data |
| `data/analysis_plots.png` | Static visualizations |

### Running the Experiment

```bash
# Install the library
pip install greenmining[energy]

# Set your GitHub token
export GITHUB_TOKEN=ghp_your_token_here

# Open the notebook
jupyter notebook experiment/beta/experiment.ipynb
```

Run all cells sequentially. The data gathering steps require a valid GitHub token
and internet access. Analysis steps operate on the collected data.
