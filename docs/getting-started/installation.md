# Installation

This guide covers all methods to install GreenMining.

---

## Requirements

- **Python**: 3.9 or higher
- **Operating System**: Linux, macOS, or Windows
- **GitHub Token**: Required for repository fetching (optional for URL analysis)

---

## Installation Methods

### Method 1: pip (Recommended)

Install from PyPI:

```bash
pip install greenmining
```

Verify installation:

```python
python -c "import greenmining; print(f'greenmining v{greenmining.__version__}')"
# Output: greenmining v1.0.4
```

### Method 2: From Source

Clone and install for development:

```bash
# Clone repository
git clone https://github.com/adam-bouafia/greenmining.git
cd greenmining

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Method 3: Docker

Run using Docker:

```bash
# Pull image
docker pull adambouafia/greenmining:latest

# Interactive Python shell
docker run -it -v $(pwd)/data:/app/data \
           adambouafia/greenmining:latest python

# Run a Python script
docker run -v $(pwd)/data:/app/data \
           -e GITHUB_TOKEN=your_token \
           adambouafia/greenmining:latest python your_script.py
```

---

## Dependencies

GreenMining automatically installs these dependencies:

| Package | Purpose |
|---------|---------|
| `PyGithub>=2.1.1` | GitHub API access |
| `PyDriller>=2.5` | Repository mining |
| `pandas>=2.2.0` | Data manipulation |
| `scipy>=1.10.0` | Statistical analysis |
| `numpy>=1.24.0` | Numerical operations |
| `python-dotenv` | Environment variable loading |
| `tqdm` | Progress bars |

### Optional Dependencies

For energy measurement features:

```bash
# CodeCarbon support
pip install codecarbon

# Full development environment
pip install greenmining[dev]
```

---

## GitHub Token Setup

A GitHub personal access token is required for the `fetch` and `pipeline` commands.

### Creating a Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes:
    - `repo` (for private repositories)
    - `public_repo` (for public repositories only)
4. Copy the generated token

### Configuring the Token

**Option 1: Environment Variable**

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**Option 2: .env File**

Create a `.env` file in your project directory:

```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**Option 3: Pass to Functions**

Pass directly to API functions:

```python
from greenmining import fetch_repositories

repos = fetch_repositories(
    github_token="ghp_xxxxxxxxxxxxxxxxxxxx",
    max_repos=10
)
```

---

## Verifying Installation

Run the following to verify everything works:

```python
# Check version
import greenmining
print(f"greenmining v{greenmining.__version__}")

# Check available exports
from greenmining import GSF_PATTERNS, GREEN_KEYWORDS, is_green_aware
print(f"{len(GSF_PATTERNS)} patterns loaded")
print(f"{len(GREEN_KEYWORDS)} keywords loaded")

# Test pattern detection
print(is_green_aware("Enable caching"))  # True
```

---

## Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'greenmining'`**

Solution: Ensure you've activated your virtual environment and installed the package:

```bash
source venv/bin/activate
pip install greenmining
```

**Issue: `GITHUB_TOKEN not set`**

Solution: Set the environment variable or create a `.env` file:

```bash
export GITHUB_TOKEN=your_token_here
```

**Issue: `Rate limit exceeded`**

Solution: GitHub API has rate limits. Either:

- Wait for the rate limit to reset (1 hour)
- Use an authenticated token for higher limits
- Reduce `--max-repos` parameter

**Issue: `Permission denied` on RAPL energy measurement**

Solution: RAPL requires root access or specific permissions:

```bash
# Grant read access to energy files
sudo chmod a+r /sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj
```

Or use CodeCarbon instead (no root needed):

```python
from greenmining.energy import CodeCarbonMeter
meter = CodeCarbonMeter()
```

---

## Next Steps

- [Quick Start Guide](quickstart.md) - Run your first analysis
- [Configuration](configuration.md) - Customize GreenMining settings
- [Python API](../user-guide/api.md) - Complete API reference
