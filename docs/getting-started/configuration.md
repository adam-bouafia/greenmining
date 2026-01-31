# Configuration

GreenMining uses direct function parameters -- no config files, no env vars, no intermediary objects.

---

## GitHub Token

The only external requirement is a **GitHub personal access token** for API access:

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

Or pass it directly in your code:

```python
from greenmining import fetch_repositories

repos = fetch_repositories(
    github_token="ghp_xxxxxxxxxxxxxxxxxxxx",
    max_repos=50,
    keywords="kubernetes",
)
```

---

## Function Parameters

### `fetch_repositories()`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `github_token` | str | (required) | GitHub personal access token |
| `max_repos` | int | 100 | Maximum repositories to fetch |
| `min_stars` | int | 100 | Minimum GitHub stars required |
| `keywords` | str | None | Search keywords for GitHub API |
| `languages` | list[str] | None | Programming language filters |
| `created_after` | str | None | Repos created after date (YYYY-MM-DD) |
| `created_before` | str | None | Repos created before date (YYYY-MM-DD) |
| `pushed_after` | str | None | Repos pushed after date (YYYY-MM-DD) |
| `pushed_before` | str | None | Repos pushed before date (YYYY-MM-DD) |
| `output_dir` | str | "./data" | Output directory for metadata |

### `clone_repositories()`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `repositories` | list | (required) | Repository objects from `fetch_repositories()` |
| `github_token` | str | None | GitHub token (optional) |
| `output_dir` | str | "./data" | Output directory for metadata |
| `cleanup_existing` | bool | False | Remove existing clones before re-cloning |

Repositories are cloned into `./greenmining_repos/` with sanitized directory names.

### `analyze_repositories()`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `urls` | list | (required) | List of GitHub repository URLs |
| `max_commits` | int | 500 | Maximum commits per repository |
| `parallel_workers` | int | 1 | Parallel analysis workers |
| `output_format` | str | "dict" | Output format (dict, json, csv) |
| `energy_tracking` | bool | False | Enable energy measurement |
| `energy_backend` | str | "rapl" | Energy backend (rapl, codecarbon, cpu_meter, auto) |
| `method_level_analysis` | bool | False | Per-method complexity metrics |
| `include_source_code` | bool | False | Include source code before/after |
| `ssh_key_path` | str | None | SSH key for private repos |
| `github_token` | str | None | Token for private HTTPS repos |
| `since_date` | str | None | Analyze commits from date (YYYY-MM-DD) |
| `to_date` | str | None | Analyze commits up to date (YYYY-MM-DD) |

---

## Next Steps

- [Quick Start](quickstart.md) - Get started with examples
- [Python API](../user-guide/api.md) - Full programmatic usage
- [GSF Patterns](../reference/patterns.md) - All 124 patterns
