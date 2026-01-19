# GreenMining Experiment

This directory contains the experimental validation of the GreenMining framework, a tool for detecting green software practices in commit messages from open-source repositories.

## Overview

The experiment analyzes commit messages from GitHub repositories to identify sustainability-related development practices using pattern matching against the Green Software Foundation (GSF) catalog.

## Experiment Configuration

| Parameter | Value |
|-----------|-------|
| Target Repositories | 100 |
| Commits per Repository | 500 (max) |
| Minimum Stars | 100 |
| Date Range | 2023-01-01 to 2025-01-01 |
| Programming Languages | Python, Java, Go, JavaScript, TypeScript, C#, Rust, Kotlin, Ruby, C++ |
| Pattern Database | GSF Catalog (120 patterns, 15 categories) |

### Search Keyword Groups

Repositories were selected using 8 keyword groups:

1. `microservices OR kubernetes OR docker`
2. `cloud-native OR serverless OR containerization`
3. `energy-efficient OR green-software OR carbon-aware`
4. `sustainable OR eco-friendly`
5. `performance-optimization OR resource-optimization`
6. `memory-efficient OR cpu-efficient`
7. `event-driven OR distributed-systems`
8. `scalable OR high-performance`

## Pipeline Stages

The experiment executes GreenMining's 5-stage pipeline:

1. **FETCH** - Discover repositories from GitHub API
2. **EXTRACT** - Extract commit messages using PyDriller
3. **ANALYZE** - Detect green patterns in commits
4. **AGGREGATE** - Compute statistics and metrics
5. **REPORT** - Generate analysis report

## Directory Structure

```
experiment/
├── README.md                           # This file
├── greenmining_experiment.ipynb        # Main experiment notebook
├── .env                                # GitHub token (not committed)
└── data/
    ├── repositories.json               # Fetched repository metadata
    ├── commits.json                    # Extracted commit messages
    ├── analysis_results.json           # Pattern detection results
    ├── aggregated_statistics.json      # Computed statistics
    └── green_software_analysis_report.md  # Generated report
```

## Requirements

```bash
pip install greenmining python-dotenv tqdm
```

## Setup

1. Create a `.env` file with your GitHub token:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```

2. Open `greenmining_experiment.ipynb` in Jupyter

3. Run all cells to execute the experiment

## Research Questions Addressed

| RQ | Question | Metrics |
|----|----------|---------|
| **RQ1** | To what extent do developers discuss energy efficiency and sustainability? | Green-aware %, temporal trend, per-language rates |
| **RQ2** | Which green software patterns are most frequently applied? | Pattern frequency, category distribution, co-occurrence |
| **RQ3** | Are there sustainability practices not documented in existing catalogs? | Novel keyword analysis, novelty ratio |

## Output

The experiment produces:

- **Data files** (JSON) - Raw and processed data
- **Statistics** - Summary metrics, per-language/repository breakdowns
- **Figures** (PDF/PNG) - Publication-ready visualizations
- **Report** (Markdown) - Complete analysis report

```

## License

This project is licensed under the MIT License 