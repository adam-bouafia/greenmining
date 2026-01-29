#!/usr/bin/env python3
import sys
import time
import json
from pathlib import Path
from datetime import datetime

print("=" * 60)
print("GreenMining Small Experiment - 5 Repos, 10 Commits Each")
print("=" * 60)
print()

# Test repositories (popular repos with varied commit history)
TEST_REPOS = [
    "https://github.com/tiangolo/fastapi",
    "https://github.com/pallets/flask", 
    "https://github.com/psf/requests",
    "https://github.com/encode/httpx",
    "https://github.com/python-poetry/poetry",
]

MAX_COMMITS = 10
OUTPUT_DIR = Path("experiment/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Import greenmining modules
print("[1/5] Importing greenmining modules...")
start = time.perf_counter()
from greenmining.services import LocalRepoAnalyzer
from greenmining.energy import RAPLEnergyMeter
from greenmining.gsf_patterns import is_green_aware, get_pattern_by_keywords
elapsed = time.perf_counter() - start
print(f"    Imports completed in {elapsed:.2f}s")
print()

# Initialize analyzer
print("[2/5] Initializing LocalRepoAnalyzer...")
analyzer = LocalRepoAnalyzer(max_commits=MAX_COMMITS)
print(f"    Analyzer configured for max {MAX_COMMITS} commits per repo")
print()

# Initialize energy meter
print("[3/5] Checking energy measurement...")
meter = RAPLEnergyMeter()
energy_available = meter.is_available()
if energy_available:
    print(f"    RAPL available: {meter.get_available_domains()}")
else:
    print("    RAPL not available, energy measurement disabled")
print()

# Run analysis
print("[4/5] Analyzing repositories...")
print("-" * 60)

results = []
total_commits = 0
green_commits = 0
patterns_found = {}

for i, url in enumerate(TEST_REPOS, 1):
    repo_name = url.split("/")[-1]
    print(f"\n  [{i}/{len(TEST_REPOS)}] {repo_name}")
    print(f"      URL: {url}")
    
    start_time = time.perf_counter()
    energy_joules = 0.0
    
    try:
        # Create fresh meter for each repo
        if energy_available:
            repo_meter = RAPLEnergyMeter()
            repo_meter.start()
        
        # Analyze repository
        repo_result = analyzer.analyze_repository(url)
        
        if energy_available:
            try:
                energy = repo_meter.stop()
                energy_joules = energy.joules
            except:
                energy_joules = 0.0
        
        elapsed = time.perf_counter() - start_time
        
        # Process results
        commits_analyzed = len(repo_result.commits)
        green_count = sum(1 for c in repo_result.commits if c.green_aware)
        
        total_commits += commits_analyzed
        green_commits += green_count
        
        # Collect patterns
        for commit in repo_result.commits:
            for pattern in commit.gsf_patterns_matched:
                patterns_found[pattern] = patterns_found.get(pattern, 0) + 1
        
        result = {
            "repository": repo_name,
            "url": url,
            "commits_analyzed": commits_analyzed,
            "green_commits": green_count,
            "green_percentage": round(green_count / commits_analyzed * 100, 1) if commits_analyzed > 0 else 0,
            "patterns": [p for c in repo_result.commits for p in c.gsf_patterns_matched],
            "analysis_time_seconds": round(elapsed, 2),
            "energy_joules": round(energy_joules, 4) if energy_joules else 0,
        }
        results.append(result)
        
        print(f"      Commits: {commits_analyzed}, Green: {green_count} ({result['green_percentage']}%)")
        print(f"      Time: {elapsed:.2f}s, Energy: {energy_joules:.4f}J")
        
    except Exception as e:
        print(f"      ERROR: {e}")
        results.append({
            "repository": repo_name,
            "url": url,
            "error": str(e),
        })

print("\n" + "-" * 60)

# Summary
print("\n[5/5] Experiment Summary")
print("=" * 60)
print(f"  Total repositories analyzed: {len([r for r in results if 'error' not in r])}")
print(f"  Total commits analyzed: {total_commits}")
print(f"  Green-aware commits: {green_commits} ({round(green_commits/total_commits*100, 1) if total_commits > 0 else 0}%)")
print()

if patterns_found:
    print("  Top patterns detected:")
    for pattern, count in sorted(patterns_found.items(), key=lambda x: -x[1])[:10]:
        print(f"    - {pattern}: {count}")
print()

# Save results
output_file = OUTPUT_DIR / f"experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, "w") as f:
    json.dump({
        "experiment_date": datetime.now().isoformat(),
        "config": {
            "max_commits_per_repo": MAX_COMMITS,
            "repositories_count": len(TEST_REPOS),
        },
        "summary": {
            "total_commits": total_commits,
            "green_commits": green_commits,
            "green_percentage": round(green_commits/total_commits*100, 1) if total_commits > 0 else 0,
            "patterns_found": patterns_found,
        },
        "results": results,
    }, f, indent=2)

print(f"  Results saved to: {output_file}")
print()
print("EXPERIMENT COMPLETED SUCCESSFULLY")
print("=" * 60)
