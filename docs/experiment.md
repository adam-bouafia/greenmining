# Experiment: Unified Repository Analysis Pipeline

This page describes the reference experiment included with GreenMining. The Jupyter notebook
(`experiment/omega/experiment.ipynb`) demonstrates every feature of the library in a single,
end-to-end pipeline applied to 13 repositories.

## Overview

The experiment follows a four-part structure:

| Part | Purpose | Library Features Used |
|------|---------|----------------------|
| **A: Setup** | Install, import, configure | `greenmining` package, `GSF_PATTERNS`, `GREEN_KEYWORDS` |
| **B: Data Gathering** | Fetch and analyze repositories | `fetch_repositories`, `analyze_repositories` |
| **C: Unified Analysis** | Apply every analyzer to the combined dataset | All 7 analyzers, energy, carbon, visualization, export |
| **D: Summary** | Feature coverage table and output files | — |

---

## Part A: Setup

### Step 1 — Install

```python
!pip install greenmining[energy,dashboard] --upgrade --quiet
```

The `[energy,dashboard]` extras install optional dependencies for energy measurement
(CodeCarbon) and the Flask web dashboard.

### Step 2 — Imports

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
    QualitativeAnalyzer,
    CodeDiffAnalyzer,
    PowerRegressionDetector,
    MetricsPowerCorrelator,
    VersionPowerAnalyzer,
)
from greenmining.energy import CarbonReporter, get_energy_meter, CPUEnergyMeter
from greenmining.dashboard import create_app
```

### Step 3 — Configuration

Shared parameters used across the entire pipeline:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `MAX_COMMITS` | 20 | Commits analyzed per repository |
| `MIN_STARS` | 3 | Minimum GitHub stars for search |
| `PARALLEL_WORKERS` | 2 | Concurrent repository analysis |
| `LANGUAGES` | 20 | Top programming languages |

The GitHub token is loaded from the environment or a `.env` file.

---

## Part B: Data Gathering

### Step 4 — Search Blockchain Repositories

Uses `fetch_repositories()` with the **GraphQL API v4** to find 10 blockchain repositories:

```python
search_repos = fetch_repositories(
    github_token=GITHUB_TOKEN,
    max_repos=10,
    min_stars=MIN_STARS,
    languages=LANGUAGES,
    keywords="blockchain",
    created_after="2020-01-01",
)
```

**Library feature:** `greenmining.fetch_repositories` wraps `GitHubGraphQLFetcher.search_repositories`.
When more than 5 languages are provided, the language filter is skipped to stay within
GitHub query complexity limits.

### Step 5 — Analyze All 13 Repositories

Combines the 10 searched repositories with 3 manually selected ones (Flask, Requests, FastAPI),
then runs the full analysis pipeline on all of them at once:

```python
results = analyze_repositories(
    urls=all_urls,           # 13 repository URLs
    max_commits=MAX_COMMITS,
    parallel_workers=PARALLEL_WORKERS,
    output_format="dict",
    energy_tracking=True,
    energy_backend="auto",
    method_level_analysis=True,
    include_source_code=True,
    github_token=GITHUB_TOKEN,
)
```

**Library features applied per repository:**

- GSF pattern detection (122 patterns, 15 categories, 321 keywords)
- Process metrics (DMM unit size, complexity, interfacing)
- Method-level analysis (per-function complexity via Lizard)
- Source code capture (before/after for each modified file)
- Energy measurement (auto-detected backend)

### Step 6 — Results Overview

Prints a summary table and builds a flat `all_commits` list used by every subsequent analysis step.

---

## Part C: Unified Analysis

Every analyzer operates on the combined dataset of all 13 repositories.

### Step 7 — GSF Pattern Analysis

Counts pattern frequency across all commits and groups patterns by category.

**Library features:** `GSF_PATTERNS` dictionary (122 patterns), category grouping.

### Step 8 — Green Awareness Detection

Demonstrates `is_green_aware()` on sample commit messages and `get_pattern_by_keywords()` for
pattern lookup.

**Library features:** `greenmining.is_green_aware`, `greenmining.get_pattern_by_keywords`.

### Step 9 — Process Metrics

Inspects DMM scores, structural complexity, and method-level data collected during analysis.

**Library features:** Process metrics from `analyze_repositories` with `method_level_analysis=True`.

| Metric | Description |
|--------|-------------|
| `dmm_unit_size` | Delta Maintainability Model — size (0-1) |
| `dmm_unit_complexity` | Delta Maintainability Model — complexity (0-1) |
| `dmm_unit_interfacing` | Delta Maintainability Model — interfacing (0-1) |
| `total_nloc` | Total non-comment lines of code |
| `total_complexity` | Cyclomatic complexity sum |
| `max_complexity` | Highest single-function complexity |
| `methods_count` | Number of methods analyzed |

### Step 10 — Statistical Analysis

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

### Step 11 — Temporal Analysis

Groups commits by quarter and tracks green awareness evolution over time:

```python
temporal = TemporalAnalyzer(granularity="quarter")
temporal_results = temporal.analyze_trends(all_commits, analysis_results_fmt)
```

**Library feature:** `greenmining.analyzers.TemporalAnalyzer`

Output includes period-by-period green commit rates, unique pattern counts, overall trend
direction, and peak period identification.

### Step 12 — Qualitative Validation

Generates stratified samples for manual review of classification accuracy:

```python
qual = QualitativeAnalyzer(sample_size=30, stratify_by="pattern")
samples = qual.generate_validation_samples(
    commits=all_commits,
    analysis_results=analysis_results_fmt,
    include_negatives=True,
)
qual.export_samples_for_review("data/validation_samples.json")
```

**Library feature:** `greenmining.analyzers.QualitativeAnalyzer`

After manual review, import validated samples and compute inter-rater reliability
with `qual.calculate_metrics()`.

### Step 13 — Code Diff Pattern Signatures

Inspects the 15+ green pattern categories that `CodeDiffAnalyzer` detects directly in code diffs:

```python
diff_analyzer = CodeDiffAnalyzer()
print(diff_analyzer.PATTERN_SIGNATURES)
```

**Library feature:** `greenmining.analyzers.CodeDiffAnalyzer`

Pattern signatures include caching, lazy loading, compression, connection pooling,
batch processing, async I/O, and more.

### Step 14 — Energy Measurement

Demonstrates all energy measurement backends and measures a sample workload:

```python
meter = CPUEnergyMeter()
result, energy = meter.measure(sample_workload)
# energy.joules, energy.watts_avg, energy.watts_peak, energy.duration_seconds
```

**Library features:** `greenmining.energy.get_energy_meter`, `CPUEnergyMeter`,
`RAPLEnergyMeter`, `CodeCarbonMeter`

| Backend | Platform | Accuracy |
|---------|----------|----------|
| RAPL | Linux (Intel/AMD) | Hardware counters |
| CodeCarbon | Cross-platform | Emission tracking |
| CPU Meter | Universal | CPU utilization + TDP estimate |
| Auto | Any | Selects best available |

### Step 15 — Carbon Footprint Reporting

Converts energy measurements to CO2 emissions using regional carbon intensity:

```python
reporter = CarbonReporter(country_iso="USA")
report = reporter.generate_report(total_joules=total_joules)
# report.total_emissions_kg, report.tree_months, report.smartphone_charges
```

**Library feature:** `greenmining.energy.CarbonReporter`

Supports 20+ countries and major cloud providers (AWS, GCP, Azure regions).

### Step 16 — Power Regression Detection

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

### Step 17 — Metrics-to-Power Correlation

Correlates code metrics (complexity, NLOC, churn) with energy consumption:

```python
correlator = MetricsPowerCorrelator(significance_level=0.05)
correlator.fit(metric_names, metrics_values, power_measurements)
summary = correlator.summary()
```

**Library feature:** `greenmining.analyzers.MetricsPowerCorrelator`

Computes Pearson and Spearman coefficients with significance testing, plus feature importance
ranking across all metrics.

### Step 18 — Version Power Analysis

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

### Step 19 — Visualization (matplotlib)

Static 2x2 chart grid:

1. Green commit rate per repository (horizontal bar)
2. Top 10 GSF patterns (horizontal bar)
3. Total vs green commit breakdown (grouped bar)
4. Complexity distribution (histogram)

Saved to `data/analysis_plots.png`.

### Step 20 — Interactive Visualization (Plotly)

Interactive charts:

- **Sunburst:** Repository > Green/Non-Green > Pattern
- **Scatter:** Complexity vs Lines of Code, colored by green awareness

### Step 21 — Export Results

Exports the combined dataset in three formats:

| Format | File | Content |
|--------|------|---------|
| JSON | `data/analysis_results.json` | Full analysis data (all fields) |
| CSV | `data/analysis_results.csv` | Flattened commit-level rows |
| DataFrame | In-memory | pandas DataFrame for further analysis |

### Step 22 — Web Dashboard

Creates a Flask-based dashboard with REST API endpoints:

```python
app = create_app(data_dir="./data")
```

**Library feature:** `greenmining.dashboard.create_app`, `greenmining.dashboard.run_dashboard`

| Endpoint | Description |
|----------|-------------|
| `GET /` | Dashboard UI |
| `GET /api/repositories` | Repository data |
| `GET /api/analysis` | Analysis results |
| `GET /api/statistics` | Aggregated statistics |
| `GET /api/energy` | Energy report |
| `GET /api/summary` | Summary metrics |

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
| Energy Measurement (auto-detected backend) | `greenmining.energy` | Yes |
| Statistical Analysis (correlations, effect sizes) | `greenmining.analyzers` | Yes |
| Temporal Analysis (quarterly trends) | `greenmining.analyzers` | Yes |
| Qualitative Validation (stratified sampling) | `greenmining.analyzers` | Yes |
| Code Diff Pattern Signatures | `greenmining.analyzers` | Yes |
| Carbon Footprint Reporting (20+ countries) | `greenmining.energy` | Yes |
| Power Regression Detection | `greenmining.analyzers` | Demonstrated |
| Metrics-to-Power Correlation (Pearson/Spearman) | `greenmining.analyzers` | Yes |
| Version Power Comparison | `greenmining.analyzers` | Demonstrated |
| Visualization (matplotlib + Plotly) | External | Yes |
| Export (JSON, CSV, DataFrame) | Built-in | Yes |
| Web Dashboard (Flask REST API) | `greenmining.dashboard` | Yes |

### Output Files

| File | Description |
|------|-------------|
| `data/analysis_results.json` | Full analysis data |
| `data/analysis_results.csv` | Flattened commit-level data |
| `data/analysis_plots.png` | Static visualizations |
| `data/validation_samples.json` | Qualitative validation samples |

### Running the Experiment

```bash
# Install the library
pip install greenmining[energy,dashboard]

# Set your GitHub token
export GITHUB_TOKEN=ghp_your_token_here

# Open the notebook
jupyter notebook experiment/omega/experiment.ipynb
```

Run all cells sequentially. The data gathering steps require a valid GitHub token
and internet access. Analysis steps operate on the collected data.
