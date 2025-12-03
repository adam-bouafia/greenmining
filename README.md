# greenmining

Green mining for microservices repositories.

[![PyPI](https://img.shields.io/pypi/v/greenmining)](https://pypi.org/project/greenmining/)
[![Python](https://img.shields.io/pypi/pyversions/greenmining)](https://pypi.org/project/greenmining/)
[![License](https://img.shields.io/github/license/adam-bouafia/greenmining)](LICENSE)

## Overview

`greenmining` is a Python library and CLI tool for analyzing GitHub repositories to identify green software engineering practices and energy-efficient patterns. It detects 122 sustainable software patterns across cloud, web, AI, database, networking, and general categories, including advanced patterns from VU Amsterdam 2024 research on green architectural tactics for ML systems.

## Features

- 🔍 **122 Sustainability Patterns**: Detect energy-efficient and environmentally conscious coding practices across 15 categories
- 📊 **Repository Mining**: Analyze 100+ microservices repositories from GitHub
- 📈 **Green Awareness Detection**: Identify sustainability-focused commits
- 📄 **Comprehensive Reports**: Generate analysis reports in multiple formats
- 🐳 **Docker Support**: Run in containers for consistent environments
- ⚡ **Fast Analysis**: Parallel processing and checkpoint system

## Installation

### Via pip

```bash
pip install greenmining
```

### From source

```bash
git clone https://github.com/adam-bouafia/greenmining.git
cd greenmining
pip install -e .
```

### With Docker

```bash
docker pull adambouafia/greenmining:latest
```

## Quick Start

### CLI Usage

```bash
# Set your GitHub token
export GITHUB_TOKEN="your_github_token"

# Run full analysis pipeline
greenmining pipeline --max-repos 100

# Fetch repositories
greenmining fetch --max-repos 100 --min-stars 100

# Extract commits
greenmining extract --max-commits 50

# Analyze for green patterns
greenmining analyze

# Generate report
greenmining report
```

### Python API

#### Basic Pattern Detection

```python
from greenmining import GSF_PATTERNS, is_green_aware, get_pattern_by_keywords

# Check available patterns
print(f"Total patterns: {len(GSF_PATTERNS)}")  # 76

# Detect green awareness in commit messages
commit_msg = "Optimize Redis caching to reduce energy consumption"
if is_green_aware(commit_msg):
    patterns = get_pattern_by_keywords(commit_msg)
    print(f"Matched patterns: {patterns}")
    # Output: ['Cache Static Data', 'Use Efficient Cache Strategies']
```

#### Analyze Repository Commits

```python
from greenmining.services.github_fetcher import GitHubFetcher
from greenmining.services.commit_extractor import CommitExtractor
from greenmining.services.data_analyzer import DataAnalyzer
from greenmining.config import Config

# Initialize services
config = Config()
fetcher = GitHubFetcher(config)
extractor = CommitExtractor(config)
analyzer = DataAnalyzer(config)

# Fetch repositories
repos = fetcher.fetch_repositories(max_repos=10, min_stars=100)

# Extract commits from first repo
commits = extractor.extract_commits(repos[0], max_commits=50)

# Analyze commits for green patterns
results = []
for commit in commits:
    result = analyzer.analyze_commit(commit)
    if result['green_aware']:
        results.append(result)
        print(f"Green commit found: {commit.message[:50]}...")
        print(f"  Patterns: {result['known_pattern']}")
```

#### Access Sustainability Patterns Data

```python
from greenmining import GSF_PATTERNS

# Get all cloud patterns
cloud_patterns = {
    pid: pattern for pid, pattern in GSF_PATTERNS.items()
    if pattern['category'] == 'cloud'
}
print(f"Cloud patterns: {len(cloud_patterns)}")

# Get pattern details
cache_pattern = GSF_PATTERNS['gsf_001']
print(f"Pattern: {cache_pattern['name']}")
print(f"Category: {cache_pattern['category']}")
print(f"Keywords: {cache_pattern['keywords']}")
print(f"Impact: {cache_pattern['sci_impact']}")
```

#### Generate Custom Reports

```python
from greenmining.services.data_aggregator import DataAggregator
from greenmining.config import Config

config = Config()
aggregator = DataAggregator(config)

# Load analysis results
results = aggregator.load_analysis_results()

# Generate statistics
stats = aggregator.calculate_statistics(results)
print(f"Total commits analyzed: {stats['total_commits']}")
print(f"Green-aware commits: {stats['green_aware_count']}")
print(f"Top patterns: {stats['top_patterns'][:5]}")

# Export to CSV
aggregator.export_to_csv(results, "output.csv")
```

#### Batch Analysis

```python
from greenmining.controllers.repository_controller import RepositoryController
from greenmining.config import Config

config = Config()
controller = RepositoryController(config)

# Run full pipeline programmatically
controller.fetch_repositories(max_repos=50)
controller.extract_commits(max_commits=100)
controller.analyze_commits()
controller.aggregate_results()
controller.generate_report()

print("Analysis complete! Check data/ directory for results.")
```

### Docker Usage

```bash
# Run analysis pipeline
docker run -v $(pwd)/data:/app/data \
           adambouafia/greenmining:latest --help

# With custom configuration
docker run -v $(pwd)/.env:/app/.env:ro \
           -v $(pwd)/data:/app/data \
           adambouafia/greenmining:latest pipeline --max-repos 50

# Interactive shell
docker run -it adambouafia/greenmining:latest /bin/bash
```

## Configuration

Create a `.env` file or set environment variables:

```bash
GITHUB_TOKEN=your_github_personal_access_token
MAX_REPOS=100
COMMITS_PER_REPO=50
OUTPUT_DIR=./data
```

## GSF Pattern Categories

**122 patterns across 15 categories:**

- **Cloud** (40 patterns): Autoscaling, serverless, right-sizing, region selection
- **Web** (15 patterns): CDN, caching, lazy loading, compression
- **AI/ML** (16 patterns): Model optimization, pruning, quantization, edge inference, batch optimization
- **Database** (9 patterns): Indexing, query optimization, connection pooling, prepared statements, views
- **Networking** (8 patterns): Protocol optimization, connection reuse, HTTP/2, gRPC
- **Network** (6 patterns): Request batching, GraphQL optimization, API gateway, circuit breaker
- **Resource** (2 patterns): Resource limits, dynamic allocation
- **Caching** (5 patterns): Multi-level caching, invalidation, data deduplication
- **Data** (2 patterns): Efficient serialization, pagination
- **Async** (3 patterns): Event-driven architecture, reactive streams, eliminate polling
- **Code** (4 patterns): Algorithm optimization, code efficiency, GC tuning
- **Monitoring** (3 patterns): Energy monitoring, performance profiling, APM
- **Microservices** (4 patterns): Service decomposition, colocation, graceful shutdown
- **Infrastructure** (4 patterns): Alpine containers, IaC, renewable energy regions
- **General** (1 pattern): Feature flags, incremental processing, precomputation

## CLI Commands

| Command | Description |
|---------|-------------|
| `fetch` | Fetch microservices repositories from GitHub |
| `extract` | Extract commit history from repositories |
| `analyze` | Analyze commits for green patterns |
| `aggregate` | Aggregate analysis results |
| `report` | Generate comprehensive report |
| `pipeline` | Run complete analysis pipeline |
| `status` | Show current analysis status |

## Output Files

All outputs are saved to the `data/` directory:

- `repositories.json` - Repository metadata
- `commits.json` - Extracted commit data
- `analysis_results.json` - Pattern analysis results
- `aggregated_statistics.json` - Summary statistics
- `green_analysis_results.csv` - CSV export for spreadsheets
- `green_microservices_analysis.md` - Final report

## Development

```bash
# Clone repository
git clone https://github.com/adam-bouafia/greenmining.git
cd greenmining

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=greenmining tests/

# Format code
black greenmining/ tests/
ruff check greenmining/ tests/
```

## Requirements

- Python 3.9+
- PyGithub >= 2.1.1
- PyDriller >= 2.5
- pandas >= 2.2.0
- click >= 8.1.7

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Links

- **GitHub**: https://github.com/adam-bouafia/greenmining
- **PyPI**: https://pypi.org/project/greenmining/
- **Docker Hub**: https://hub.docker.com/r/adambouafia/greenmining
- **Documentation**: https://github.com/adam-bouafia/greenmining#readme


