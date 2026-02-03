# Changelog

## [1.2.8] - 2026-02-03

### Changed
- Documentation audit: updated all docs to match library v1.2.x API
- Removed references to deleted Config class, CommitExtractor, GitHubFetcher
- Updated experiment.md to match actual beta notebook (10 repos, cloud domain)
- Fixed installation.md version number

### Fixed
- url-analysis.md Config import references (Config class was removed in v1.2.0)
- library-reference.md CommitExtractor documentation (class was removed)
- Redacted exposed GitHub PAT from notebook cell output

## [1.2.7] - 2026-02-03

### Fixed
- Notebook pip install version sync issue

## [1.2.6] - 2026-02-03

### Added
- Notebook kernel configuration for experiment.ipynb
- Improved energy tracking output formatting

### Fixed
- Package version sync between PyPI and local development

## [1.2.5] - 2026-02-02

### Added
- `shallow_clone` parameter (default: True) to significantly reduce repository download size
- `clone_depth` parameter for custom clone depth (auto-calculated as `max(50, max_commits * 3)` if None)
- Manual git shallow cloning before PyDriller analysis for dramatic performance improvement

### Changed
- Repository cloning now uses `git clone --depth=N` by default, reducing download times by ~90%
- Clone depth automatically calculated based on max_commits to ensure sufficient history

### Performance
- Reduced clone size from 528 MB to ~50 MB for typical 10-repo analysis (90% reduction)
- Example: ant-design repo reduced from 184 MB (full) to 14 MB (depth=50) - 92% smaller
- Analysis time for small experiments reduced from 6+ minutes to under 1 minute

## [1.2.4] - 2026-02-01

### Added
- `skip_merges` parameter exposed in `analyze_repositories()` API (default: True)
- `commit_order` parameter to control commit traversal order: "newest_first" (default) or "oldest_first"

### Changed
- Commit analysis now configurable between newest-first (recent trends) and oldest-first (evolution studies)

## [1.2.3] - 2026-02-01

### Fixed
- `cleanup_after` parameter not exposed in top-level `analyze_repositories()` API
- Repositories with empty commit histories no longer included in analysis results

### Changed
- Experiment notebook updated with full Android-domain pipeline run and results

## [1.2.1] - 2026-02-01

### Fixed
- Clone directory collision in `LocalRepoAnalyzer` when multiple repos share the same name (e.g. `open-android/Android` vs `hmkcode/Android` vs `duckduckgo/Android`)
- Race condition corruption during parallel analysis (`could not lock config file` errors)
- Aligned clone path sanitization with `RepositoryController._sanitize_repo_name` (owner\_repo format)

### Changed
- Clone directory structure now uses unique `owner_repo/` parent dirs per repository

## [1.2.0] - 2026-01-31

### Added
- `clone_repositories()` top-level function for cloning repos into `./greenmining_repos/` with sanitized directory names
- Repository name sanitization (`_sanitize_repo_name`) to prevent filesystem issues from special characters
- 2 missing official GSF patterns: "Match Utilization Requirements with Pre-configured Servers", "Optimize Impact on Customer Devices and Equipment"
- 11 new green keywords (energy proportionality, backward compatible, customer device, device lifetime, etc.)
- GSF pattern database now covers 100% of the official Green Software Foundation catalog (61/61)

### Changed
- Repositories now clone to `./greenmining_repos/` instead of `/tmp` (fixes OS cleanup and permission issues)
- `fetch_repositories()` takes direct parameters -- no Config intermediary
- All function defaults are explicit parameters instead of config file values
- Default supported languages updated from 7 to 20 (matches experiment scope)
- Library reference documentation added to mkdocs navigation

### Removed
- **`config.py`** module entirely (Config class, get_config singleton, .env/YAML loading layer)
- **`__version__.py`** (stale orphaned file with wrong version 1.0.5)
- **`services/github_fetcher.py`** (empty deprecated REST API stub)
- **`analyzers/power_regression.py`** (PowerRegressionDetector -- requires running repo code, not feasible in current pipeline)
- **`analyzers/version_power_analyzer.py`** (VersionPowerAnalyzer -- same reason)
- **`analyzers/qualitative_analyzer.py`** (QualitativeAnalyzer -- unused)
- **`presenters/`** module (ConsolePresenter -- never used by any code)
- **`docs/reference/config-options.md`** (obsolete config reference page)
- 10 dead utility functions (estimate_tokens, estimate_cost, print_banner, print_section, load_csv_file, handle_github_rate_limit, format_duration, truncate_text, create_checkpoint, load_checkpoint)
- 35+ unused Config attributes that were set but never read
- Dead imports across 14 files
- Dead methods: DataAnalyzer._check_green_awareness, DataAnalyzer._detect_known_pattern, CommitExtractor._extract_commit_metadata, StatisticalAnalyzer.pattern_adoption_rate_analysis, CodeCarbonMeter.get_carbon_intensity, Config.validate

## [1.1.9] - 2026-01-31

### Removed
- Web dashboard module (`greenmining/dashboard/`) and Flask dependency
- Dashboard documentation page and all dashboard references

### Fixed
- ReadTheDocs experiment page not rendering (trailing whitespace in mkdocs nav)
- Plotly rendering in notebook (nbformat dependency)

## [1.1.6] - 2026-01-31

### Fixed
- EnergyMetrics property aliases (`energy_joules`, `average_power_watts`)
- Parallel energy measurement conflict with shared meter instance
- StatisticalAnalyzer timezone-aware date handling
- DataFrame column collision in pattern correlation analysis

### Added
- `since_date` / `to_date` parameters for date-bounded commit analysis
- `created_before` / `pushed_after` search filters
- GraphQL API and experiment documentation pages
- Full process metrics and method-level metrics documentation

### Changed
- Energy measurement demonstrates all 4 backends: RAPL, CPU Meter, CodeCarbon, tracemalloc
- Removed all PyDriller references (replaced with gitpython + lizard)

### Removed
- Qualitative Validation and Carbon Footprint Reporting steps from experiment

## [0.1.12] - 2025-12-03

### Added
- Custom search keywords for repository fetching (`--keywords` option)
- `fetch_repositories()` function exposed in public API

### Changed
- README updated to reflect 122 patterns (was showing 76 in PyPI description)

## [0.1.11] - 2025-12-03

### Added
- Expanded pattern database from 76 to 122 patterns
- Added 9 new categories
- Expanded keywords from 190 to 321
- VU Amsterdam 2024 research patterns for ML systems

## [0.1.0] - 2025-12-02

### Added
- Initial release
- Core functionality for GSF pattern mining
- Support for 100 microservices repositories
- Pattern matching with 76 GSF patterns
- Green awareness analysis
- Docker containerization

[1.2.8]: https://github.com/adam-bouafia/greenmining/compare/v1.2.7...v1.2.8
[1.2.7]: https://github.com/adam-bouafia/greenmining/compare/v1.2.6...v1.2.7
[1.2.6]: https://github.com/adam-bouafia/greenmining/compare/v1.2.5...v1.2.6
[1.2.5]: https://github.com/adam-bouafia/greenmining/compare/v1.2.4...v1.2.5
[1.2.4]: https://github.com/adam-bouafia/greenmining/compare/v1.2.3...v1.2.4
[1.2.3]: https://github.com/adam-bouafia/greenmining/compare/v1.2.1...v1.2.3
[1.2.1]: https://github.com/adam-bouafia/greenmining/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/adam-bouafia/greenmining/compare/v1.1.9...v1.2.0
[1.1.9]: https://github.com/adam-bouafia/greenmining/compare/v1.1.6...v1.1.9
[1.1.6]: https://github.com/adam-bouafia/greenmining/compare/v0.1.12...v1.1.6
[0.1.12]: https://github.com/adam-bouafia/greenmining/compare/v0.1.11...v0.1.12
[0.1.11]: https://github.com/adam-bouafia/greenmining/compare/v0.1.0...v0.1.11
[0.1.0]: https://github.com/adam-bouafia/greenmining/releases/tag/v0.1.0
