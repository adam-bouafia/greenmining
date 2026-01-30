# Web Dashboard

Interactive web dashboard for exploring GreenMining analysis results.

---

## Overview

GreenMining includes a Flask-based dashboard that reads analysis data from a directory
and presents it through a web UI with REST API endpoints. Install with:

```bash
pip install greenmining[dashboard]
```

---

## Quick Start

```python
from greenmining.dashboard import create_app, run_dashboard

# Option 1: Run directly
run_dashboard(data_dir="./data", host="127.0.0.1", port=5000)

# Option 2: Get the Flask app (for custom configuration)
app = create_app(data_dir="./data")
app.run(host="127.0.0.1", port=5000)
```

Then open `http://127.0.0.1:5000` in your browser.

---

## Functions

### create_app()

Create a Flask application instance.

```python
def create_app(data_dir: str = "./data") -> Flask
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data_dir` | str | `"./data"` | Path to directory containing analysis JSON files |

**Returns:** Flask application instance.

The app looks for these JSON files in `data_dir`:

| File | Used By |
|------|---------|
| `repositories.json` | `/api/repositories` |
| `analysis_results.json` | `/api/analysis`, `/api/summary` |
| `aggregated_statistics.json` | `/api/statistics` |
| `energy_report.json` | `/api/energy` |

Files are loaded on each request, so you can update them while the dashboard is running.

### run_dashboard()

Start the dashboard server.

```python
def run_dashboard(
    data_dir: str = "./data",
    host: str = "127.0.0.1",
    port: int = 5000,
) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data_dir` | str | `"./data"` | Path to analysis data directory |
| `host` | str | `"127.0.0.1"` | Host to bind to |
| `port` | int | `5000` | Port to bind to |

---

## REST API Endpoints

All endpoints return JSON responses.

### GET /

Returns the dashboard HTML page with embedded JavaScript. The page fetches data
from the API endpoints below and renders summary cards and a repository table.

### GET /api/repositories

Returns repository data from `repositories.json`.

**Response:**

```json
{
  "total_repositories": 13,
  "repositories": [
    {
      "name": "flask",
      "full_name": "pallets/flask",
      "language": "Python",
      "stars": 68000,
      "description": "The Python micro framework..."
    }
  ]
}
```

### GET /api/analysis

Returns analysis results from `analysis_results.json`.

**Response:** Full analysis data including per-repository results, commits,
patterns matched, and metrics.

### GET /api/statistics

Returns aggregated statistics from `aggregated_statistics.json`.

**Response:** Statistical summaries including pattern distributions, temporal
trends, and correlation data.

### GET /api/energy

Returns energy measurement data from `energy_report.json`.

**Response:** Energy consumption metrics, carbon footprint data, and
backend information.

### GET /api/summary

Computed on-the-fly from `repositories.json` and `analysis_results.json`.

**Response:**

```json
{
  "repositories": 13,
  "commits_analyzed": 260,
  "green_commits": 42,
  "green_rate": 16.2
}
```

---

## Data Preparation

The dashboard reads JSON files produced by the analysis pipeline. To populate the
data directory, run an analysis first:

```python
from greenmining import analyze_repositories
import json

results = analyze_repositories(
    urls=["https://github.com/pallets/flask"],
    max_commits=100,
    energy_tracking=True,
)

# Save for the dashboard
with open("data/analysis_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
```

Or use the experiment notebook which exports all required files automatically.

---

## Integration with Jupyter

The dashboard app can be created inside a notebook for inspection, but should be
run from a terminal for actual use:

```python
# In a notebook cell (inspect only)
from greenmining.dashboard import create_app
app = create_app(data_dir="./data")
print("Dashboard created. Run from terminal:")
print("  from greenmining.dashboard import run_dashboard")
print('  run_dashboard(data_dir="./data")')
```

```bash
# From terminal
python -c "from greenmining.dashboard import run_dashboard; run_dashboard()"
```

---

## Next Steps

- [Python API](api.md) - Full API reference
- [Energy Measurement](energy.md) - Energy backends and carbon reporting
- [Experiment](../examples/experiment.md) - Full pipeline walkthrough
