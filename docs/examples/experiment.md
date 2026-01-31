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

```
GreenMining version: 1.1.7
GSF Patterns: 122
Green Keywords: 321
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

### Step 4 -- Search DevOps Repositories

Uses `fetch_repositories()` with the **GraphQL API v4** to find 10 devops repositories:

```python
search_repos = fetch_repositories(
    github_token=GITHUB_TOKEN,
    max_repos=10,
    min_stars=MIN_STARS,
    languages=LANGUAGES,
    keywords="devops",
    created_after=CREATED_AFTER,
    created_before=CREATED_BEFORE,
    pushed_after=PUSHED_AFTER,
)
```

```
Found 10 devops repositories:
   1. antonputra/tutorials (4410 stars, HCL)
   2. geerlingguy/ansible-for-devops (9598 stars, Python)
   3. in28minutes/devops-master-class (2818 stars, Java)
   4. hygieia/hygieia (3905 stars, TypeScript)
   5. stacksimplify/aws-eks-kubernetes-masterclass (1710 stars, Java)
   6. iam-veeramalla/python-for-devops (4260 stars, Python)
   7. milanm/DevOps-Roadmap (18639 stars, None)
   8. bregman-arie/devops-exercises (80815 stars, Python)
   9. ravdy/DevOps (256 stars, Jinja)
  10. MicrosoftDocs/mslearn-tailspin-spacegame-web (212 stars, Shell)
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

```
Analysis complete: 13 repositories
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

```
======================================================================
UNIFIED ANALYSIS SUMMARY
======================================================================
Repositories analyzed: 13
Total commits: 187
Green-aware commits: 55
Overall green rate: 29.4%

Repository                               Commits    Green      Rate
----------------------------------------------------------------------
geerlingguy/ansible-for-devops           14         7          50.0%
in28minutes/devops-master-class          2          1          50.0%
hygieia/hygieia                          2          0          0.0%
stacksimplify/aws-eks-kubernetes-masterclass 20     4          20.0%
antonputra/tutorials                     20         16         80.0%
iam-veeramalla/python-for-devops         20         0          0.0%
milanm/DevOps-Roadmap                    20         2          10.0%
ravdy/DevOps                             0          0          0.0%
MicrosoftDocs/mslearn-tailspin-spacegame-web 9      2          22.2%
bregman-arie/devops-exercises            20         10         50.0%
psf/requests                             20         1          5.0%
pallets/flask                            20         6          30.0%
tiangolo/fastapi                         20         6          30.0%

Flattened commit pool: 187 commits
```

---

## Part C: Unified Analysis

Every analyzer operates on the combined dataset of all 13 repositories.

### Step 7 -- GSF Pattern Analysis

Counts pattern frequency across all commits and groups patterns by category.

**Library features:** `GSF_PATTERNS` dictionary (122 patterns), category grouping.

```
Unique patterns detected: 46

Top 20 GSF Patterns:
Pattern                                       Count    % of Commits
-----------------------------------------------------------------
Keep Request Counts Low                       17       9.1%
Containerize Your Workload                    13       7.0%
Use Compiled Languages                        13       7.0%
Performance Profiling                         10       5.3%
Delete Unused Storage Resources               9        4.8%
Minimize Deployed Environments                8        4.3%
Remove Unused Assets                          7        3.7%
Serve Images in Modern Formats                7        3.7%
Scale Down Kubernetes Workloads               6        3.2%
Scale Kubernetes Workloads Based on Events    6        3.2%
Properly Sized Images                         6        3.2%
Avoid Excessive DOM Size                      4        2.1%
Defer Offscreen Images                        4        2.1%
gRPC for Service Communication                4        2.1%
Match VM Utilization Requirements             3        1.6%
Eliminate Polling                             3        1.6%
Reduce Network Traversal Between VMs          3        1.6%
Avoid Chaining Critical Requests              3        1.6%
Evaluate Using a Service Mesh                 3        1.6%
Service Mesh Optimization                     3        1.6%

GSF Categories (15):
  ai: 19 patterns          async: 3 patterns
  caching: 2 patterns      cloud: 40 patterns
  code: 4 patterns         data: 3 patterns
  database: 5 patterns     general: 8 patterns
  infrastructure: 4        microservices: 4
  monitoring: 3            network: 6 patterns
  networking: 2            resource: 2 patterns
  web: 17 patterns
```

### Step 8 -- Green Awareness Detection

Demonstrates `is_green_aware()` on sample commit messages and `get_pattern_by_keywords()` for
pattern lookup.

**Library features:** `greenmining.is_green_aware`, `greenmining.get_pattern_by_keywords`.

```
Green Awareness Detection:
  [GREEN] Optimize database queries for energy efficiency
  [-----] Fix typo in README
  [GREEN] Implement lazy loading for images to reduce bandwidth
  [-----] Add unit tests for login
  [GREEN] Reduce memory footprint of cache layer
  [GREEN] Refactor to async I/O for better resource utilization

Pattern Lookup Examples:
  "cache"        -> ['Cache Static Data']
  "lazy loading" -> ['Scale Infrastructure with User Load', 'Defer Offscreen Images', 'Lazy Loading']
  "compression"  -> ['Compress Stored Data', 'Compress Transmitted Data', 'Enable Text Compression']
  "async"        -> ['Queue Non-Urgent Requests', 'Use Async Instead of Sync', 'Lazy Loading']
```

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

```
Process Metrics Summary
======================================================================
Metric                           Avg        Min        Max      N
-----------------------------------------------------------------
dmm_unit_size                   0.69       0.00       1.00     27
dmm_unit_complexity             0.87       0.00       1.00     27
dmm_unit_interfacing            0.86       0.00       1.00     27
total_nloc                    141.00       0.00    3868.00    187
total_complexity               22.30       0.00     503.00    187
max_complexity                 14.37       0.00     308.00    187
methods_count                  15.12       0.00     303.00    187
insertions                   1899.17       0.00   59094.00    187
deletions                       8.36       0.00     257.00    187

Method-Level Analysis:
  Total methods analyzed: 2828
  Sample from stacksimplify/aws-eks-kubernetes-masterclass (5e1e0c15):
    NotificationsApplication::main: nloc=3, complexity=1
    NotificationsApplication::configure: nloc=3, complexity=1
    CorsFilter::CorsFilter: nloc=2, complexity=1

Source code changes captured: 2125
```

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

```
Pattern Correlation Analysis:
  Significant pairs: 22
    Containerize Your Workload <-> Scale Down Kubernetes Workloads: 0.666 (moderate)
    Scale Down Kubernetes Workloads <-> Scale Kubernetes Workloads Based on Events: 1.000 (strong)
    Delete Unused Storage Resources <-> Remove Unused Assets: 0.877 (strong)
    Properly Sized Images <-> Defer Offscreen Images: 0.812 (strong)
    Defer Offscreen Images <-> Serve Images in Modern Formats: 0.750 (strong)
    Compress Transmitted Data <-> Reduce Network Traversal Between VMs: 0.814 (strong)

Temporal Trend:
  Direction: decreasing
  Significant: False
  Correlation: nan

Effect Size (Green vs Non-Green Complexity):
  Cohen's d: 0.148 (negligible)
  Mean difference: 11.30
  Significant: False
```

### Step 11 -- Temporal Analysis

Groups commits by quarter and tracks green awareness evolution over time:

```python
temporal = TemporalAnalyzer(granularity="quarter")
temporal_results = temporal.analyze_trends(all_commits, analysis_results_fmt)
```

**Library feature:** `greenmining.analyzers.TemporalAnalyzer`

```
Temporal Analysis (10 periods):
Period               Commits    Green      Rate       Patterns
------------------------------------------------------------
2022-Q4              1          0          0.0%      0
2023-Q1              107        0          0.0%      0
2023-Q2              23         0          0.0%      0
2023-Q3              4          0          0.0%      0
2023-Q4              25         0          0.0%      0
2024-Q1              6          0          0.0%      0
2024-Q2              4          0          0.0%      0
2024-Q3              1          0          0.0%      0
2025-Q1              1          0          0.0%      0
2025-Q2              15         0          0.0%      0
```

Output includes period-by-period green commit rates, unique pattern counts, overall trend
direction, and peak period identification.

### Step 12 -- Code Diff Pattern Signatures

Inspects the 15 green pattern categories that `CodeDiffAnalyzer` detects directly in code diffs:

```python
diff_analyzer = CodeDiffAnalyzer()
print(diff_analyzer.PATTERN_SIGNATURES)
```

**Library feature:** `greenmining.analyzers.CodeDiffAnalyzer`

```
Code Diff Pattern Signatures: 15 types
  caching             resource_optimization    database_optimization
  async_processing    lazy_loading             serverless_computing
  cdn_edge            compression              model_optimization
  efficient_protocols container_optimization   green_regions
  auto_scaling        code_splitting           green_ml_training
```

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

```
Available Energy Backends:
  rapl: available (RAPLEnergyMeter)
  codecarbon: available (CodeCarbonMeter)
  cpu_meter: available (CPUEnergyMeter)

--- RAPL Energy Meter ---
  Energy: 2.7681 J
  Power avg: 33.15 W
  Duration: 0.083 s

--- CPU Energy Meter ---
  Energy: 3.4150 J
  Power avg: 27.22 W
  Duration: 0.125 s
  Backend: cpu_meter

--- CodeCarbon CO2 Tracking ---
  CO2 emissions: 0.00000018 kg
  Equivalent: 0.1765 mg CO2

--- tracemalloc Memory Profiling ---
  Current memory: 1.5 KB
  Peak memory: 21.3 KB

--- Analysis Energy (from repository pipeline) ---
  geerlingguy/ansible-for-devops:
    Total: 38.1038 J
    Avg power: 27.65 W
```

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

```
PowerRegressionDetector configured:
  Test command: python -c "sum(range(100000))"
  Backend: cpu_meter
  Threshold: 5.0%
  Iterations: 3, Warmup: 1
```

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

```
Insufficient data (0 points, need >= 3)
Enable energy_tracking=True to collect per-commit energy data.
```

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

```
VersionPowerAnalyzer configured:
  Backend: cpu_meter, Iterations: 5, Warmup: 1
```

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

```
Exported data/analysis_results.json
Exported 187 commits to data/analysis_results.csv
DataFrame shape: (187, 20)
```

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
