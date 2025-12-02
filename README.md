# Green Microservices Mining CLI

Interactive CLI tool for mining GitHub repositories to analyze green software engineering practices in microservices architectures.

## Overview

This tool fetches top microservice repositories from GitHub, extracts commit data, analyzes commits for energy efficiency and sustainability practices and generates comprehensive reports for academic research.

## Features

- 🔍 **Repository Mining**: Fetch top 100+ microservice repositories from GitHub
- 📊 **Commit Analysis**: Extract and analyze commit history for green practices
- 📈 **Pattern Detection**: Identify known and emerging green software patterns
- 📄 **Report Generation**: Generate academic-ready markdown reports with statistics
- 💾 **Multiple Output Formats**: CSV, JSON, and Markdown outputs
- ⚡ **Resume Capability**: Checkpoint system for long-running analyses

## Installation

### Prerequisites

- Python 3.10 or higher
- GitHub Personal Access Token

### Setup

```bash
# Clone or create project directory
cd /home/neo/Documents/greenmining

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Environment Configuration

Edit `.env` file:

```env
GITHUB_TOKEN=your_github_personal_access_token
MAX_REPOS=100
COMMITS_PER_REPO=50
OUTPUT_DIR=./data
```

## Usage

### Full Pipeline

Run the complete analysis pipeline:

```bash
python cli.py pipeline
```

### Individual Commands

Run specific phases:

```bash
# Fetch repositories
python cli.py fetch --max-repos 100 --min-stars 100

# Extract commits
python cli.py extract --max-commits 50 --skip-merges

# Analyze with Claude
python cli.py analyze --batch-size 10 --resume

# Aggregate results
python cli.py aggregate

# Generate report
python cli.py report

# Check status
python cli.py status
```

### Command Options

#### `fetch`
- `--max-repos`: Maximum number of repositories to fetch (default: 100)
- `--min-stars`: Minimum stars required (default: 100)
- `--languages`: Comma-separated language list (default: java,python,go,nodejs,csharp)

#### `extract`
- `--max-commits`: Maximum commits per repository (default: 50)
- `--skip-merges`: Skip merge commits (default: true)
- `--days-back`: Only analyze commits from last N days (default: 730)

#### `analyze`
- `--batch-size`: Number of commits to analyze in parallel (default: 10)
- `--resume`: Resume from last checkpoint

#### Global Options
- `--config`: Path to custom .env file
- `--verbose`: Enable verbose logging
- `--dry-run`: Show what would be done without executing

## Project Structure

```
green-microservices-mining/
├── venv/                         # Virtual environment
├── .env                          # Environment configuration (not in git)
├── .gitignore
├── requirements.txt              # Python dependencies
├── config.py                     # Configuration management
├── utils.py                      # Helper functions
├── github_fetcher.py             # Repository fetching
├── commit_extractor.py           # Commit extraction
├── data_analyzer.py              # Data analysis
├── data_aggregator.py            # Data aggregation
├── reports.py                    # Report generation
├── cli.py                        # CLI interface
├── main.py                       # Entry point
├── data/                         # Output directory
│   ├── repositories.json
│   ├── commits.json
│   ├── analysis_results.json
│   ├── aggregated_statistics.json
│   ├── green_analysis_results.csv
│   └── green_microservices_analysis.md
└── README.md
```

## Output Files

- `repositories.json`: Metadata of fetched repositories
- `commits.json`: Extracted commit data
- `analysis_results.json`: Claude analysis results per commit
- `aggregated_statistics.json`: Summary statistics
- `green_analysis_results.csv`: Tabular data for spreadsheet analysis
- `green_microservices_analysis.md`: Final academic report

## Research Questions

This tool answers the assignment questions:

1. **Q1: Green Awareness** - Do developers of microservice-based open-source projects discuss or address energy efficiency and sustainability in their commits?
   - Method: Keyword matching against 40+ green software terms
   - Keywords: energy, power, carbon, optimization, efficient, etc.

2. **Q2: Known GSF Patterns** - Are known green software patterns and tactics being applied?
   - Method: Pattern matching against Green Software Foundation catalog
   - Source: https://patterns.greensoftware.foundation/
   - Categories: Cloud, Web, AI, Networking, Database, General
   - Patterns: 20+ official GSF patterns including:
     - Caching (Redis, CDN, Memcache)
     - Autoscaling & Right-sizing
     - Serverless Computing
     - Lazy Loading & Asynchronous Processing
     - Connection & Resource Pooling
     - Database Optimization & Indexing
     - ML Model Optimization
     - And more...

3. **Q3: Emerging Practices** - Discover new possible green patterns/tactics not yet documented
   - Method: Manual review of commits showing green awareness but not matching known patterns
   - Focus: Microservice-specific sustainability practices

## License

MIT License - See LICENSE file for details

## Contributing

This is a research tool. For issues or suggestions, please open an issue.

## Citation

If you use this tool in your research, please cite:

```
[Your thesis citation here]
```

## Acknowledgments

Built with:
- PyGithub for GitHub API
- Click for CLI framework
- pandas for data processing
