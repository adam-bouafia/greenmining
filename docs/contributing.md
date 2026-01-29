# Contributing to GreenMining

Thank you for your interest in contributing to GreenMining! 

---

## Getting Started

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/greenmining.git
cd greenmining
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install in development mode
pip install -e ".[dev]"
```

### 3. Run Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=greenmining --cov-report=html

# Specific test file
pytest tests/test_gsf_patterns.py -v
```

---

## Development Guidelines

### Code Style

We follow PEP 8 with these tools:

```bash
# Format code
black greenmining/ tests/

# Check types
mypy greenmining/

# Lint
ruff check greenmining/
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

Configuration (`.pre-commit-config.yaml`):

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
```

---

## Contribution Types

### 🐛 Bug Reports

1. Search existing issues first
2. Create a new issue with:
   - GreenMining version (`pip show greenmining`)
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/tracebacks

### ✨ Feature Requests

1. Check existing issues and roadmap
2. Create an issue describing:
   - Use case
   - Proposed solution
   - Alternatives considered

### 📝 Documentation

- Fix typos and clarify explanations
- Add examples
- Improve docstrings
- Update README

### 🔧 Code Contributions

1. Open an issue to discuss major changes
2. Fork and create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

---

## Adding New GSF Patterns

### 1. Update Pattern Definition

Edit `greenmining/gsf_patterns.py`:

```python
GSF_PATTERNS = {
    # ... existing patterns ...
    
    "new_pattern_key": {
        "name": "New Pattern Name",
        "category": "category_name",  # cloud, web, ai, caching, etc.
        "keywords": ["keyword1", "keyword2", "keyword3"],
        "description": "Brief description of the pattern",
        "sci_impact": "How this pattern reduces software carbon intensity"
    },
}
```

### 2. Add Keywords to GREEN_KEYWORDS

```python
GREEN_KEYWORDS = [
    # ... existing keywords ...
    "keyword1",
    "keyword2", 
    "keyword3",
]
```

### 3. Write Tests

```python
# tests/test_gsf_patterns.py

def test_new_pattern_detection():
    """Test that new pattern is detected correctly."""
    from greenmining import is_green_aware, get_pattern_by_keywords
    
    # Should detect
    assert is_green_aware("message with keyword1")
    patterns = get_pattern_by_keywords("message with keyword1")
    assert "New Pattern Name" in patterns
    
    # Should not detect
    assert not is_green_aware("unrelated message")
```

### 4. Update Documentation

Add pattern to `docs/reference/patterns.md`

---

## Project Structure

```
greenmining/
├── __init__.py          # Package exports
├── __main__.py          # Entry point
├── config.py            # Configuration
├── gsf_patterns.py      # Pattern definitions
├── utils.py             # Utilities
├── analyzers/           # Analysis modules
│   ├── qualitative_analyzer.py
│   ├── statistical_analyzer.py
│   └── temporal_analyzer.py
├── controllers/         # Controllers
│   └── repository_controller.py
├── energy/              # Energy measurement
│   ├── base.py
│   ├── rapl_backend.py
│   └── codecarbon_backend.py
├── models/              # Data models
├── presenters/          # Output formatting
│   └── console_presenter.py
└── services/            # Core services
    ├── commit_extractor.py
    ├── data_aggregator.py
    ├── data_analyzer.py
    ├── github_fetcher.py
    ├── local_repo_analyzer.py
    └── reports.py
```

---

## Pull Request Process

### 1. Create Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Changes

- Write clean, documented code
- Add tests for new functionality
- Update documentation if needed

### 3. Commit with Clear Messages

```bash
git add .
git commit -m "feat: add new pattern detection for X"
# or
git commit -m "fix: resolve issue with Y"
# or
git commit -m "docs: update installation instructions"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Code refactoring
- `chore:` - Maintenance

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title
- Description of changes
- Link to related issue
- Screenshots if UI changes

### 5. Address Review Feedback

Respond to reviewer comments and make requested changes.

---

## Testing Guidelines

### Test Structure

```python
# tests/test_module.py

import pytest
from greenmining import function_to_test

class TestFunctionName:
    """Tests for function_to_test."""
    
    def test_basic_functionality(self):
        """Test basic happy path."""
        result = function_to_test("input")
        assert result == "expected"
    
    def test_edge_case(self):
        """Test edge case handling."""
        result = function_to_test("")
        assert result is None
    
    def test_error_handling(self):
        """Test error conditions."""
        with pytest.raises(ValueError):
            function_to_test(None)
```

### Running Tests

```bash
# All tests
pytest

# Verbose output
pytest -v

# Specific test
pytest tests/test_gsf_patterns.py::test_pattern_detection -v

# With coverage
pytest --cov=greenmining --cov-report=html
open htmlcov/index.html
```

---

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers
- Acknowledge contributions

---

## Getting Help

- 📖 [Documentation](https://greenmining.readthedocs.io)
- 💬 [GitHub Discussions](https://github.com/adam-bouafia/greenmining/discussions)
- 🐛 [Issue Tracker](https://github.com/adam-bouafia/greenmining/issues)

---

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.
