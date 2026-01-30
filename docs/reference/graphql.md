# GraphQL API Reference

GreenMining uses GitHub's GraphQL API v4 for repository search and metadata retrieval.

---

## Overview

The `GitHubGraphQLFetcher` class provides efficient repository discovery using a single
GraphQL query per page of results, compared to multiple REST API calls.

```python
from greenmining.services.github_graphql_fetcher import GitHubGraphQLFetcher

fetcher = GitHubGraphQLFetcher(token="ghp_your_token")
```

Or use the top-level wrapper:

```python
from greenmining import fetch_repositories

repos = fetch_repositories(
    github_token="ghp_your_token",
    max_repos=10,
    keywords="blockchain",
)
```

---

## GitHubGraphQLFetcher

### Constructor

```python
GitHubGraphQLFetcher(token: str)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `token` | str | GitHub personal access token with `repo` scope |

### search_repositories()

Search for repositories matching criteria.

```python
def search_repositories(
    keywords: str = "microservices",
    max_repos: int = 100,
    min_stars: int = 100,
    languages: list[str] | None = None,
    created_after: str | None = None,
    created_before: str | None = None,
    pushed_after: str | None = None,
    pushed_before: str | None = None,
) -> list[Repository]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `keywords` | str | `"microservices"` | Search keywords |
| `max_repos` | int | `100` | Maximum repositories to return |
| `min_stars` | int | `100` | Minimum GitHub stars |
| `languages` | list | `None` | Filter by programming languages |
| `created_after` | str | `None` | Created after date (YYYY-MM-DD) |
| `created_before` | str | `None` | Created before date (YYYY-MM-DD) |
| `pushed_after` | str | `None` | Last pushed after date (YYYY-MM-DD) |
| `pushed_before` | str | `None` | Last pushed before date (YYYY-MM-DD) |

**Returns:** List of `Repository` objects.

**Example:**

```python
fetcher = GitHubGraphQLFetcher(token)

repos = fetcher.search_repositories(
    keywords="blockchain",
    max_repos=10,
    min_stars=3,
    languages=["Python", "Go", "Rust"],
    created_after="2020-01-01",
)

for repo in repos:
    print(f"{repo.full_name} ({repo.stars} stars, {repo.language})")
```

### get_repository_commits()

Fetch commits for a specific repository.

```python
def get_repository_commits(
    owner: str,
    name: str,
    max_commits: int = 100,
) -> list[dict]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `owner` | str | (required) | Repository owner |
| `name` | str | (required) | Repository name |
| `max_commits` | int | `100` | Maximum commits to fetch |

**Returns:** List of commit dictionaries with keys:

| Key | Type | Description |
|-----|------|-------------|
| `sha` | str | Commit SHA (oid) |
| `message` | str | Commit message |
| `date` | str | Committed date (ISO 8601) |
| `author` | str | Author name |
| `author_email` | str | Author email |
| `additions` | int | Lines added |
| `deletions` | int | Lines deleted |
| `changed_files` | int | Number of files changed |

**Example:**

```python
commits = fetcher.get_repository_commits("pallets", "flask", max_commits=50)
for c in commits:
    print(f"{c['sha'][:8]} | {c['author']} | {c['message'][:60]}")
```

### save_results()

Save repositories to a JSON file.

```python
def save_results(repositories: list[Repository], output_file: str) -> None
```

---

## Search Query Building

The `_build_search_query()` method constructs a GitHub search query string from the
parameters. Understanding how queries are built helps debug search results.

### Query Format

```
{keywords} stars:>={min_stars} [language:{lang}]... [created:>={date}] [pushed:>={date}]
```

### Language Filter Limit

GitHub's search API has a complexity limit on queries. When more than 5 languages
are specified, the language filter is **skipped entirely** to avoid empty results:

```python
# 3 languages -> filter applied
# Query: "blockchain stars:>=3 language:Python language:Go language:Rust"
repos = fetch_repositories(languages=["Python", "Go", "Rust"], ...)

# 20 languages -> filter skipped (returns repos in any language)
# Query: "blockchain stars:>=3"
repos = fetch_repositories(languages=LANGUAGES_20, ...)
```

This is by design. When using many languages, the search returns results in any language,
which is more useful than returning zero results from an overly complex query.

### Date Filters

All date filters use the `YYYY-MM-DD` format:

```python
# Repos created in 2023
repos = fetcher.search_repositories(
    created_after="2023-01-01",
    created_before="2023-12-31",
)

# Repos with recent activity
repos = fetcher.search_repositories(
    pushed_after="2024-01-01",
)
```

---

## Rate Limiting

The GraphQL API has a point-based rate limit (5,000 points/hour for authenticated users).
Each search query costs 1 point.

GreenMining handles rate limits automatically:

- Prints remaining quota after each query
- Sleeps for 60 seconds when remaining points drop below 100
- Supports pagination with cursor-based `after` parameter

```
Rate Limit: 4998/5000 (cost: 1)
```

### Checking Your Rate Limit

```python
fetcher = GitHubGraphQLFetcher(token)
# Rate limit info is printed with every query
repos = fetcher.search_repositories(max_repos=1)
```

---

## Pagination

Results are paginated using GitHub's cursor-based pagination. The fetcher handles
this automatically:

- Fetches up to 100 results per page (GitHub's maximum)
- Follows `pageInfo.hasNextPage` and `endCursor` cursors
- Stops when `max_repos` is reached or no more results exist

For large result sets:

```python
# Fetches 3 pages of 100 results each
repos = fetcher.search_repositories(max_repos=300)
```

---

## Repository Model

Each search result is parsed into a `Repository` dataclass:

| Field | Type | Source (GraphQL) |
|-------|------|------------------|
| `repo_id` | int | Sequential index |
| `name` | str | `name` |
| `owner` | str | Parsed from `nameWithOwner` |
| `full_name` | str | `nameWithOwner` |
| `url` | str | `url` |
| `clone_url` | str | `url` + `.git` |
| `language` | str | `primaryLanguage.name` |
| `stars` | int | `stargazerCount` |
| `forks` | int | `forkCount` |
| `watchers` | int | `watchers.totalCount` |
| `open_issues` | int | 0 (not queried) |
| `last_updated` | str | `updatedAt` |
| `created_at` | str | `createdAt` |
| `description` | str | `description` |
| `main_branch` | str | `defaultBranchRef.name` |
| `archived` | bool | `isArchived` |
| `license` | str | `licenseInfo.name` |

---

## GraphQL Query Schema

The search query fetches these fields per repository:

```graphql
query($searchQuery: String!, $first: Int!) {
  search(query: $searchQuery, type: REPOSITORY, first: $first) {
    repositoryCount
    pageInfo { hasNextPage, endCursor }
    nodes {
      ... on Repository {
        id, name, nameWithOwner, description, url
        createdAt, updatedAt, pushedAt
        stargazerCount, forkCount
        watchers { totalCount }
        primaryLanguage { name }
        languages(first: 5) { nodes { name } }
        licenseInfo { name }
        isArchived, isFork
        defaultBranchRef { name }
      }
    }
  }
  rateLimit { limit, cost, remaining, resetAt }
}
```

---

## Next Steps

- [Python API](../user-guide/api.md) - `fetch_repositories` wrapper
- [Data Models](models.md) - Repository dataclass fields
- [Experiment](../experiment.md) - Full pipeline example
