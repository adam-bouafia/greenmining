import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Check if greenmining is installed
try:
    import greenmining
    print(f"✓ Using greenmining version: {greenmining.__version__}")
except ImportError:
    print("✗ greenmining not installed!")
    print("\nPlease install with: pip install greenmining")
    sys.exit(1)

from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

# Import from greenmining package
from greenmining import fetch_repositories
from greenmining.services.commit_extractor import CommitExtractor
from greenmining.services.data_analyzer import DataAnalyzer
from greenmining.services.data_aggregator import DataAggregator

print("=" * 80)
print("GREENMINING EXPERIMENT - PyPI Package")
print("=" * 80)

# Configuration
EXPERIMENT_CONFIG = {
    "repos": 100,
    "commits_per_repo": 1000,
    "min_stars": 10,
    "keywords": "software engineering",
    "enable_nlp": True,
    "enable_ml": True,
    "enable_temporal": True,
    "enable_enhanced_stats": True,
    "temporal_granularity": "quarter",
}

print("\n📋 Experiment Configuration:")
print(f"  • Repositories: {EXPERIMENT_CONFIG['repos']}")
print(f"  • Commits per repo: {EXPERIMENT_CONFIG['commits_per_repo']}")
print(f"  • Minimum stars: {EXPERIMENT_CONFIG['min_stars']}")
print(f"  • Keywords: {EXPERIMENT_CONFIG['keywords']}")
print(f"  • NLP Analysis: {'✓' if EXPERIMENT_CONFIG['enable_nlp'] else '✗'}")
print(f"  • ML Features: {'✓' if EXPERIMENT_CONFIG['enable_ml'] else '✗'}")
print(f"  • Temporal Analysis: {'✓' if EXPERIMENT_CONFIG['enable_temporal'] else '✗'}")
print(f"  • Enhanced Stats: {'✓' if EXPERIMENT_CONFIG['enable_enhanced_stats'] else '✗'}")

# Get GitHub token
token = os.getenv("GITHUB_TOKEN")
if not token:
    print("\n✗ GITHUB_TOKEN not found in environment")
    print("Please set GITHUB_TOKEN in .env file")
    sys.exit(1)

print(f"\n✓ GitHub token found")

# Create output directory
output_dir = Path(__file__).parent / "results_pypi"
output_dir.mkdir(exist_ok=True)
print(f"✓ Output directory: {output_dir}")

# Metadata
metadata = {
    "experiment_date": datetime.now().isoformat(),
    "greenmining_version": greenmining.__version__,
    "config": EXPERIMENT_CONFIG,
}

# ============================================================================
# STAGE 1: Fetch Repositories
# ============================================================================
print("\n" + "=" * 80)
print("STAGE 1/5: Fetching Repositories")
print("=" * 80)

stage1_start = time.time()

try:
    repositories = fetch_repositories(
        github_token=token,
        max_repos=EXPERIMENT_CONFIG["repos"],
        min_stars=EXPERIMENT_CONFIG["min_stars"],
        keywords=EXPERIMENT_CONFIG["keywords"],
    )
    
    stage1_elapsed = time.time() - stage1_start
    
    print(f"\n✅ Stage 1 Complete in {stage1_elapsed:.1f}s")
    print(f"   Fetched: {len(repositories)} repositories")
    
    # Show sample
    print(f"\n   Sample repositories:")
    for repo in repositories[:5]:
        print(f"     • {repo.full_name} ({repo.stars} ⭐, {repo.language or 'N/A'})")
    if len(repositories) > 5:
        print(f"     ... and {len(repositories) - 5} more")
    
    metadata["stage1"] = {
        "duration_seconds": stage1_elapsed,
        "repos_fetched": len(repositories),
    }
    
except Exception as e:
    print(f"\n❌ Stage 1 Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# STAGE 2: Extract Commits
# ============================================================================
print("\n" + "=" * 80)
print("STAGE 2/5: Extracting Commits")
print("=" * 80)

stage2_start = time.time()

try:
    extractor = CommitExtractor(
        github_token=token,
        max_commits=EXPERIMENT_CONFIG["commits_per_repo"],
        skip_merges=True,
        days_back=730,
        timeout=120,
    )
    
    # This should work with Repository objects (fixed in v1.0.2)
    all_commits = extractor.extract_from_repositories(repositories)
    
    stage2_elapsed = time.time() - stage2_start
    
    print(f"\n✅ Stage 2 Complete in {stage2_elapsed:.1f}s ({stage2_elapsed/60:.1f}m)")
    print(f"   Extracted: {len(all_commits)} commits")
    print(f"   Average: {len(all_commits)/len(repositories):.1f} commits/repo")
    
    # Save commits
    extractor.save_results(
        all_commits,
        output_dir / "commits.json",
        len(repositories)
    )
    print(f"   Saved: {output_dir / 'commits.json'}")
    
    metadata["stage2"] = {
        "duration_seconds": stage2_elapsed,
        "commits_extracted": len(all_commits),
        "avg_commits_per_repo": len(all_commits) / len(repositories),
    }
    
except Exception as e:
    print(f"\n❌ Stage 2 Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# STAGE 3: Analyze Commits
# ============================================================================
print("\n" + "=" * 80)
print("STAGE 3/5: Analyzing Commits")
print("=" * 80)

stage3_start = time.time()

try:
    analyzer = DataAnalyzer(
        enable_nlp=EXPERIMENT_CONFIG["enable_nlp"],
        enable_ml_features=EXPERIMENT_CONFIG["enable_ml"],
        enable_diff_analysis=False,  # Too slow for large experiments
    )
    
    analyzed_commits = analyzer.analyze_commits(all_commits)
    
    stage3_elapsed = time.time() - stage3_start
    
    # Count green-aware commits
    green_count = sum(1 for c in analyzed_commits if c.get("green_aware", False))
    green_percentage = (green_count / len(analyzed_commits) * 100) if analyzed_commits else 0
    
    print(f"\n✅ Stage 3 Complete in {stage3_elapsed:.1f}s")
    print(f"   Analyzed: {len(analyzed_commits)} commits")
    print(f"   Green-aware: {green_count} ({green_percentage:.1f}%)")
    
    # Save analysis
    analyzer.save_results(analyzed_commits, output_dir / "analyzed.json")
    print(f"   Saved: {output_dir / 'analyzed.json'}")
    
    metadata["stage3"] = {
        "duration_seconds": stage3_elapsed,
        "commits_analyzed": len(analyzed_commits),
        "green_aware_count": green_count,
        "green_aware_percentage": green_percentage,
    }
    
except Exception as e:
    print(f"\n❌ Stage 3 Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# STAGE 4: Aggregate Results
# ============================================================================
print("\n" + "=" * 80)
print("STAGE 4/5: Aggregating Results")
print("=" * 80)

stage4_start = time.time()

try:
    aggregator = DataAggregator(
        enable_enhanced_stats=EXPERIMENT_CONFIG["enable_enhanced_stats"],
        enable_temporal=EXPERIMENT_CONFIG["enable_temporal"],
        temporal_granularity=EXPERIMENT_CONFIG["temporal_granularity"],
    )
    
    # This should work with Repository objects (fixed in v1.0.2)
    results = aggregator.aggregate(analyzed_commits, repositories)
    
    stage4_elapsed = time.time() - stage4_start
    
    print(f"\n✅ Stage 4 Complete in {stage4_elapsed:.1f}s")
    
    metadata["stage4"] = {
        "duration_seconds": stage4_elapsed,
    }
    
except Exception as e:
    print(f"\n❌ Stage 4 Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# STAGE 5: Save Results and Generate Report
# ============================================================================
print("\n" + "=" * 80)
print("STAGE 5/5: Saving Results")
print("=" * 80)

try:
    # Save aggregated results
    aggregator.save_results(
        results,
        output_dir / "aggregated.json",
        output_dir / "aggregated.csv",
        analyzed_commits
    )
    print(f"✓ Saved: {output_dir / 'aggregated.json'}")
    print(f"✓ Saved: {output_dir / 'aggregated.csv'}")
    
    # Save metadata
    import json
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Saved: {output_dir / 'metadata.json'}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("EXPERIMENT SUMMARY")
    print("=" * 80)
    
    aggregator.print_summary(results)
    
    # Total time
    total_time = sum([
        metadata["stage1"]["duration_seconds"],
        metadata["stage2"]["duration_seconds"],
        metadata["stage3"]["duration_seconds"],
        metadata["stage4"]["duration_seconds"],
    ])
    
    print(f"\n⏱ Total Time: {total_time:.1f}s ({total_time/60:.1f}m)")
    print(f"\n📁 Results saved in: {output_dir.absolute()}")
    
except Exception as e:
    print(f"\n❌ Stage 5 Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ EXPERIMENT COMPLETE!")
print("=" * 80)
print(f"\n🎉 Successfully analyzed {len(repositories)} repositories")
print(f"   with {len(all_commits)} commits using greenmining v{greenmining.__version__}")
