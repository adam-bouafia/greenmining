# Greenmining Experiment: Software Engineering Repository Analysis

This experiment analyzes 100 software engineering repositories with 1000 commits each, using all available analysis features.

## Setup

1. **Install greenmining from PyPI**:
   ```bash
   pip install greenmining
   ```

2. **Set GitHub Token**:
   ```bash
   export GITHUB_TOKEN="your_github_personal_access_token"
   ```

3. **Run the experiment**:
   ```bash
   python run_experiment.py
   ```

## Experiment Parameters

- **Repositories**: 100
- **Commits per repo**: 1000
- **Minimum stars**: 10
- **Languages**: All (no filter)
- **Search keywords**: "software engineering"

## Analysis Features (ALL ENABLED)

- ✅ NLP Analysis (morphological variants, synonyms)
- ✅ ML Feature Extraction
- ✅ Temporal Trend Analysis (quarterly)
- ✅ Enhanced Statistical Analysis
- ⚠️ Code Diff Analysis (disabled - too slow for 100K commits)

## Expected Outputs

All results will be saved to `./data/`:

- `repositories.json` - Fetched repository metadata
- `commits.json` - Extracted commits (~100,000 commits)
- `analysis_results.json` - Pattern detection results
- `aggregated_statistics.json` - Statistical summary
- `experiment_report.md` - Comprehensive report
- `experiment_metadata.json` - Experiment configuration and timing

**Total: 2-3 hours**

## Troubleshooting

### Rate Limiting
If you hit GitHub API rate limits:
```bash
# Check your rate limit status
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit
```

### Memory Issues
If analysis fails with memory errors, reduce batch size or commit count in the script.
