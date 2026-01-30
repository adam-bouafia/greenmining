# Roadmap & Future Work

This document outlines planned features and enhancements for GreenMining.

---

## Current Status (v1.0.5 Beta)

### Implemented Features

| Feature | Status | Description |
|---------|--------|-------------|
| **GSF Pattern Catalog** | Complete | 122 patterns across 15 categories |
| **GitHub Repository Mining** | Complete | GraphQL API with filters |
| **URL-Based Analysis** | Complete | Direct PyDriller analysis |
| **Commit Classification** | Complete | Keyword matching with confidence |
| **Energy Measurement** | Complete | RAPL + CodeCarbon backends |
| **Statistical Analysis** | Complete | Correlations, effect sizes, trends |
| **Temporal Analysis** | Complete | Configurable time granularity |
| **Report Generation** | Complete | JSON, CSV, Markdown outputs |
| **DMM Metrics** | Complete | Delta Maintainability Model |
| **Process Metrics** | Complete | All 8 PyDriller process metrics |
| **Configuration-Based URL Input** | Complete | YAML config with sources.urls |
| **Batch URL Analysis API** | Complete | LocalRepoAnalyzer.analyze_repositories with parallel workers |
| **Private Repository Support** | Complete | SSH key and GitHub token authentication |
| **CPU Energy Meter Backend** | Complete | CPUEnergyMeter class with auto-detection |
| **Integrated Energy Tracking** | Complete | LocalRepoAnalyzer energy_tracking parameter |
| **Carbon Footprint Reporting** | Complete | CarbonReporter class with 20+ country profiles |
| **Method-Level Analysis** | Complete | method_level_analysis parameter |
| **Source Code Access** | Complete | include_source_code parameter |
| **Power Regression Detection** | Complete | PowerRegressionDetector class |
| **Metrics-to-Power Correlation** | Complete | MetricsPowerCorrelator class |
| **Version-by-Version Power Analysis** | Complete | VersionPowerAnalyzer class |
| **Web Dashboard** | Complete | Flask-based dashboard module |

---

## Phase 1: Enhanced Repository Support (Priority: High)

### 1.1 Configuration-Based URL Input

Support for specifying repository URLs directly in configuration files.

```yaml
# greenmining.yaml
sources:
  urls:
    - https://github.com/kubernetes/kubernetes
    - https://github.com/istio/istio
    - git@github.com:company/private-repo.git
  search:
    enabled: true
    keywords: "microservices cloud-native"
    min_stars: 500
```

**Status:** Complete
**Effort:** Low
**Impact:** High

### 1.2 Batch URL Analysis API

Dedicated function for analyzing multiple repositories.

```python
from greenmining import analyze_repositories

results = analyze_repositories(
    urls=[
        "https://github.com/kubernetes/kubernetes",
        "https://github.com/istio/istio",
    ],
    max_commits=100,
    parallel_workers=4,
    output_format="json"
)
```

**Status:** Complete
**Effort:** Medium
**Impact:** High

### 1.3 Private Repository Support

Authentication for private repositories via SSH keys or tokens.

```python
from greenmining.services import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer(
    ssh_key_path="~/.ssh/id_rsa",
    github_token="ghp_xxx"  # For private GitHub repos
)
result = analyzer.analyze_repository("git@github.com:company/private-repo.git")
```

**Status:** Complete
**Effort:** Medium
**Impact:** Medium

---

## Phase 2: Extended Energy Measurement (Priority: High)

### 2.1 CPU Energy Meter Backend

Cross-platform CPU energy measurement support.

```python
from greenmining.energy import CPUEnergyMeter

meter = CPUEnergyMeter(
    backend="auto"  # auto-detect: RAPL, Windows EEE, Apple Silicon
)
with meter.measure() as metrics:
    result = analyzer.analyze_repository(url)
```

**Platforms:**
- Complete: Linux (RAPL)
- Not Started: Windows Energy Estimation Engine
- Not Started: Apple Silicon power metrics
- Not Started: AMD Energy Driver

**Status:** Complete
**Effort:** High
**Impact:** High

### 2.2 Integrated Energy Tracking

Automatic energy tracking during analysis without manual setup.

```python
from greenmining.services import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer(energy_tracking=True, energy_backend="rapl")
result = analyzer.analyze_repository("https://github.com/flask")

print(result["energy_metrics"]["energy_joules"])
print(result["energy_metrics"]["average_power_watts"])
print(result["energy_metrics"]["duration_seconds"])
```

**Status:** Complete
**Effort:** Medium
**Impact:** High

### 2.3 Carbon Footprint Reporting

Generate carbon emissions reports based on energy measurements.

```python
from greenmining.energy import CarbonReporter

reporter = CarbonReporter(
    country_iso="USA",
    cloud_provider="aws",
    region="us-east-1"
)
report = reporter.generate_report(analysis_results)
print(f"CO2 emissions: {report.total_emissions_kg:.4f} kg")
print(f"Equivalent: {report.tree_months:.1f} tree-months")
```

**Status:** Complete
**Effort:** Low
**Impact:** Medium

---

## Phase 3: Full PyDriller Integration (Priority: Medium)

### 3.1 Complete Process Metrics

All PyDriller process metrics are integrated.

```python
from greenmining.services import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer(process_metrics="full")
result = analyzer.analyze_repository(url)

# Available metrics:
# - change_set: Files modified together
# - code_churn: Lines added/removed over time
# - commits_count: Per-file commit frequency
# - contributors_count: Unique contributors per file
# - contributors_experience: Developer expertise
# - hunks_count: Contiguous change regions
# - lines_count: Total lines in files
```

**Status:** Complete
**Effort:** Medium
**Impact:** Medium

### 3.2 Method-Level Analysis

Per-method metrics extraction using Lizard integration.

```python
result = analyzer.analyze_repository(
    url="https://github.com/flask",
    method_level_analysis=True
)

for commit in result["commits"]:
    for method in commit["methods_modified"]:
        print(f"{method['name']}: complexity={method['complexity']}")
        print(f"  params={method['parameters']}, tokens={method['token_count']}")
```

**Status:** Complete
**Effort:** High
**Impact:** Medium

### 3.3 Source Code Access

Access full source code before/after for refactoring detection.

```python
for commit in result["commits"]:
    for file in commit["modified_files"]:
        if file["source_code_before"]:
            # Analyze code transformations
            detect_refactorings(
                before=file["source_code_before"],
                after=file["source_code"]
            )
```

**Status:** Complete
**Effort:** Low
**Impact:** Low

---

## Phase 4: Green MSR Techniques (Priority: Medium)

### 4.1 Power Regression Detection

Identify commits that increased power consumption.

```python
from greenmining.analyzers import PowerRegressionDetector

detector = PowerRegressionDetector(
    test_command="pytest tests/ -x",
    energy_backend="rapl",
    threshold_percent=5.0,
    iterations=5
)
regressions = detector.detect(
    repo_path="/path/to/repo",
    baseline_commit="v1.0.0",
    target_commit="HEAD"
)

for regression in regressions:
    print(f"Commit {regression.sha[:8]}: +{regression.power_increase:.1f}%")
    print(f"  Message: {regression.message}")
```

**Status:** Complete
**Effort:** High
**Impact:** High

### 4.2 Metrics-to-Power Correlation

Build models correlating code metrics with power consumption.

```python
from greenmining.analyzers import MetricsPowerCorrelator

correlator = MetricsPowerCorrelator()
correlator.fit(
    metrics=["complexity", "nloc", "code_churn", "method_count"],
    power_measurements=measured_power_data
)

# Results
print(f"Pearson correlations: {correlator.pearson}")
print(f"Spearman correlations: {correlator.spearman}")
print(f"Feature importance: {correlator.feature_importance}")
```

**Status:** Complete
**Effort:** High
**Impact:** High

### 4.3 Version-by-Version Power Analysis

Measure power consumption across multiple software versions.

```python
from greenmining.analyzers import VersionPowerAnalyzer

analyzer = VersionPowerAnalyzer(
    test_command="pytest tests/",
    energy_backend="rapl",
    iterations=10
)
report = analyzer.analyze_versions(
    repo_path="/path/to/repo",
    versions=["v1.0", "v1.1", "v1.2", "v2.0"],
    warmup_iterations=2
)

# Visualize trends
report.plot_power_evolution("power_evolution.png")
```

**Status:** Complete
**Effort:** High
**Impact:** High

---

## Phase 5: Advanced Features (Priority: Low)

### 5.1 CI/CD Integration

GitHub Action for green energy gates.

```yaml
# .github/workflows/energy-check.yml
name: Energy Check
on: [push, pull_request]

jobs:
  energy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: adam-bouafia/greenmining-action@v1
        with:
          test_command: pytest tests/
          energy_threshold: 5%  # Max increase allowed
          fail_on_regression: true
          baseline: main
```

**Status:** Not Started
**Effort:** Medium
**Impact:** High

### 5.2 VS Code Extension

Real-time green pattern suggestions in IDE.

- Highlight code that could benefit from green patterns
- Suggest optimizations based on GSF catalog
- Show energy impact estimates
- Quick-fix actions for common patterns

**Status:** Not Started
**Effort:** High
**Impact:** Medium

### 5.3 Web Dashboard

Interactive visualization of analysis results.

- Repository comparison charts
- Pattern distribution sunbursts
- Temporal trend graphs
- Energy consumption heatmaps
- Export to various formats

**Status:** Complete
**Effort:** High
**Impact:** Medium

### 5.4 ML-Based Pattern Detection

Machine learning for pattern detection without relying on commit messages.

```python
from greenmining.ml import PatternPredictor

predictor = PatternPredictor.load("pretrained-v1")
patterns = predictor.predict_from_diff(diff_content)
# Returns patterns based on code structure, not just keywords
```

**Status:** Not Started
**Effort:** Very High
**Impact:** High

---

## Implementation Priority Matrix

| Phase | Feature | Effort | Impact | Status |
|-------|---------|--------|--------|--------|
| 1 | URL Config Support | Low | High | Complete |
| 1 | Batch URL Analysis | Medium | High | Complete |
| 1 | Private Repository Support | Medium | Medium | Complete |
| 2 | CPU Energy Meter Backend | High | High | Complete |
| 2 | Integrated Energy Tracking | Medium | High | Complete |
| 2 | Carbon Reporting | Low | Medium | Complete |
| 3 | Full Process Metrics | Medium | Medium | Complete |
| 3 | Method-Level Analysis | High | Medium | Complete |
| 3 | Source Code Access | Low | Low | Complete |
| 4 | Power Regression Detection | High | High | Complete |
| 4 | Metrics-to-Power Correlation | High | High | Complete |
| 4 | Version-by-Version Power Analysis | High | High | Complete |
| 5 | Web Dashboard | High | Medium | Complete |
| 5 | CI/CD Integration | Medium | High | Not Started |
| 5 | VS Code Extension | High | Medium | Not Started |
| 5 | ML Pattern Detection | Very High | High | Not Started |

---

## Contributing

We welcome contributions! If you'd like to help implement any of these features:

1. Check the [Contributing Guide](contributing.md)
2. Open an issue to discuss your approach
3. Submit a pull request

Priority areas for contribution:
- Phase 5 features (CI/CD, VS Code Extension, ML Detection)
- Additional GSF patterns
- Documentation improvements

---

## Version History

See [Changelog](changelog.md) for release notes.
