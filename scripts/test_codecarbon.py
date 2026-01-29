#!/usr/bin/env python3
import sys
import time
import json
from pathlib import Path
from datetime import datetime

print("=" * 60)
print("CodeCarbon Experiment - 1 Repo, 10 Commits")
print("=" * 60)
print()

TEST_REPO = "https://github.com/pallets/flask"
MAX_COMMITS = 10
OUTPUT_DIR = Path("experiment/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Import modules
print("[1/4] Importing modules...")
from greenmining.services import LocalRepoAnalyzer
from greenmining.energy import CodeCarbonMeter, RAPLEnergyMeter

# Verify CodeCarbon is available
print("[2/4] Verifying CodeCarbon...")
cc_meter = CodeCarbonMeter()
rapl_meter = RAPLEnergyMeter()

print(f"    CodeCarbonMeter available: {cc_meter.is_available()}")
print(f"    RAPLEnergyMeter available: {rapl_meter.is_available()}")

if not cc_meter.is_available():
    print("    ERROR: CodeCarbon not available!")
    sys.exit(1)

print()

# Initialize analyzer
print("[3/4] Analyzing repository with CodeCarbon...")
print("-" * 60)
analyzer = LocalRepoAnalyzer(max_commits=MAX_COMMITS)
repo_name = TEST_REPO.split("/")[-1]
print(f"    Repository: {repo_name}")
print(f"    URL: {TEST_REPO}")
print()

# Start CodeCarbon measurement
print("    Starting CodeCarbon tracker...")
cc_meter.start()
start_time = time.perf_counter()

# Analyze
repo_result = analyzer.analyze_repository(TEST_REPO)

# Stop measurement
elapsed = time.perf_counter() - start_time
cc_metrics = cc_meter.stop()

print()
print("-" * 60)

# Results
commits_analyzed = len(repo_result.commits)
green_count = sum(1 for c in repo_result.commits if c.green_aware)
patterns = {}
for commit in repo_result.commits:
    for p in commit.gsf_patterns_matched:
        patterns[p] = patterns.get(p, 0) + 1

print()
print("[4/4] Results")
print("=" * 60)
print(f"  Commits analyzed: {commits_analyzed}")
print(f"  Green-aware: {green_count} ({round(green_count/commits_analyzed*100, 1)}%)")
print(f"  Analysis time: {elapsed:.2f}s")
print()
print("  CodeCarbon Metrics:")
print(f"    Energy (Joules): {cc_metrics.joules:.4f}")
print(f"    CPU Energy (J): {cc_metrics.cpu_energy_joules:.4f}")
print(f"    DRAM Energy (J): {cc_metrics.dram_energy_joules:.4f}")
print(f"    Avg Power (W): {cc_metrics.watts_avg:.4f}")
print(f"    Duration (s): {cc_metrics.duration_seconds:.2f}")
if cc_metrics.carbon_grams:
    print(f"    Carbon (gCO2): {cc_metrics.carbon_grams:.4f}")
if cc_metrics.carbon_intensity:
    print(f"    Carbon Intensity (gCO2/kWh): {cc_metrics.carbon_intensity:.2f}")
print()

if patterns:
    print("  Patterns detected:")
    for p, count in sorted(patterns.items(), key=lambda x: -x[1])[:5]:
        print(f"    - {p}: {count}")
print()

# Save results
output_file = OUTPUT_DIR / f"codecarbon_experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, "w") as f:
    json.dump({
        "experiment_date": datetime.now().isoformat(),
        "backend": "codecarbon",
        "repository": repo_name,
        "url": TEST_REPO,
        "commits_analyzed": commits_analyzed,
        "green_commits": green_count,
        "green_percentage": round(green_count/commits_analyzed*100, 1),
        "patterns": patterns,
        "energy_metrics": cc_metrics.to_dict(),
        "analysis_time_seconds": round(elapsed, 2),
    }, f, indent=2, default=str)

print(f"  Results saved: {output_file}")
print()
print("CODECARBON EXPERIMENT COMPLETED SUCCESSFULLY")
print("=" * 60)
