# GreenMining Documentation

<p align="center">
  <strong>A Python library for mining and analyzing green software engineering patterns in GitHub repositories</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/greenmining/"><img src="https://img.shields.io/pypi/v/greenmining.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/greenmining/"><img src="https://img.shields.io/pypi/pyversions/greenmining.svg" alt="Python versions"></a>
  <a href="https://github.com/adam-bouafia/greenmining/blob/main/LICENSE"><img src="https://img.shields.io/github/license/adam-bouafia/greenmining.svg" alt="License"></a>
</p>

---

## What is GreenMining?

GreenMining is a research-grade tool for analyzing software repositories to detect **green software engineering practices**. It identifies commits that implement sustainability patterns based on the [Green Software Foundation (GSF)](https://patterns.greensoftware.foundation/) catalog.

### Key Capabilities

| Feature | Description |
|---------|-------------|
| **122 GSF Patterns** | Detect patterns across 15 categories (cloud, web, AI, caching, etc.) |
| **321 Green Keywords** | Comprehensive keyword matching for green-aware commits |
| **GitHub Mining** | Fetch repositories by keywords, stars, language filters |
| **URL Analysis** | Analyze any GitHub repo directly via URL using PyDriller |
| **Statistical Analysis** | Pattern correlations, temporal trends, effect sizes |
| **Energy Measurement** | RAPL and CodeCarbon backends for power profiling |
| **Multiple Outputs** | JSON, CSV, and Markdown reports |

---

## Quick Start

### Installation

```bash
pip install greenmining
```

### Basic Usage

**Python API:**

```python
from greenmining import GSF_PATTERNS, is_green_aware, get_pattern_by_keywords

# Check if a commit message is green-aware
message = "Optimize Redis caching to reduce energy consumption"
print(is_green_aware(message))  # True

# Get matched patterns
patterns = get_pattern_by_keywords(message)
print(patterns)  # ['Cache Static Data']
```

**Analyze a Repository:**

```python
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

analyzer = LocalRepoAnalyzer()
result = analyzer.analyze_repository("https://github.com/pallets/flask")

print(f"Green-aware: {result['green_aware_percentage']:.1f}%")
```

---

## Pattern Categories

GreenMining detects **122 patterns** across **15 categories**:

| Category | Patterns | Examples |
|----------|----------|----------|
| Cloud | 40+ | Caching, compression, auto-scaling, serverless |
| Web | 15+ | Lazy loading, image optimization, minification |
| AI/ML | 10+ | Model optimization, quantization, efficient training |
| Caching | 8 | Redis, CDN, static data caching |
| Async | 6 | Batch processing, queue-based architecture |
| Database | 8 | Query optimization, connection pooling |
| Network | 6 | Compression, CDN, efficient protocols |
| Resource | 5 | Memory management, CPU optimization |
| Code | 4 | Dead code removal, algorithm efficiency |
| Infrastructure | 4 | Container optimization, IaC |
| Microservices | 4 | Service decomposition, graceful shutdown |
| Monitoring | 3 | Efficient logging, metrics collection |
| General | 8 | Feature flags, incremental processing |

---

## Documentation Sections

### Getting Started

- [Installation](getting-started/installation.md) - Install GreenMining via pip, source, or Docker
- [Quick Start](getting-started/quickstart.md) - Run your first analysis in 5 minutes
- [Configuration](getting-started/configuration.md) - Configure via environment variables or config files

### User Guide

- [Python API](user-guide/api.md) - Use GreenMining programmatically
- [URL Analysis](user-guide/url-analysis.md) - Analyze repositories directly by URL
- [Energy Measurement](user-guide/energy.md) - Measure energy consumption with RAPL/CodeCarbon

### Reference

- [GSF Patterns](reference/patterns.md) - All 122 patterns with categories and keywords
- [Configuration Options](reference/config-options.md) - All configuration parameters
- [Data Models](reference/models.md) - Repository, Commit, and AnalysisResult models

### Examples

- [Basic Usage](examples/basic.md) - Simple pattern detection examples
- [Complete Pipeline](examples/pipeline.md) - Full research workflow example

---

## Example Output

When analyzing a repository, GreenMining produces reports like:

```
============================================================
GREENMINING ANALYSIS RESULTS
============================================================

Repository: kubernetes/kubernetes
Commits analyzed: 1000
Green-aware commits: 247 (24.7%)

Top Patterns Detected:
  1. Cache Static Data (89 commits)
  2. Use Async Instead of Sync (67 commits)
  3. Containerize Workload (45 commits)
  4. Compress Transmitted Data (31 commits)

Categories Distribution:
  cloud: 45.2%
  caching: 23.1%
  async: 18.5%
  infrastructure: 13.2%
```

---

## Research Applications

GreenMining is designed for software engineering research:

- **Mining Software Repositories (MSR)** studies on green practices
- **Green Software Foundation** pattern adoption analysis
- **Temporal trend analysis** of sustainability practices
- **Cross-repository comparison** of green awareness
- **Energy measurement** of analysis workloads

---

## Citation

If you use GreenMining in your research, please cite:

```bibtex
@software{greenmining2024,
  author = {Bouafia, Adam},
  title = {GreenMining: Mining Green Software Patterns},
  year = {2024},
  url = {https://github.com/adam-bouafia/greenmining}
}
```

---

## License

GreenMining is released under the [MIT License](https://github.com/adam-bouafia/greenmining/blob/main/LICENSE).
