# Energy Measurement

Measure energy consumption of your analysis workloads with RAPL and CodeCarbon.

---

## Overview

GreenMining includes energy measurement capabilities to profile the power consumption of analysis operations. This is useful for:

- **Research** - Quantify energy cost of mining operations
- **Optimization** - Identify energy-intensive analysis steps
- **Reporting** - Include energy metrics in analysis reports

### Supported Backends

| Backend | Platform | Features |
|---------|----------|----------|
| **RAPL** | Linux (Intel/AMD) | Direct CPU/DRAM power reading |
| **CodeCarbon** | Cross-platform | Emissions tracking, cloud support |
| **CPU Energy Meter** | Linux | Alternative to RAPL (future) |

---

## RAPL Backend

Intel's Running Average Power Limit (RAPL) provides direct power measurements on Linux systems with Intel or AMD processors.

### Requirements

- Linux operating system
- Intel Core 2nd generation+ or AMD Ryzen
- Read access to `/sys/class/powercap/intel-rapl/`

### Checking Availability

```python
from greenmining.energy.rapl import RAPLEnergyMeter

meter = RAPLEnergyMeter()
if meter.is_available():
    print("RAPL is available on this system")
else:
    print("RAPL not available - try running as root")
```

### Basic Usage

```python
from greenmining.energy.rapl import RAPLEnergyMeter

meter = RAPLEnergyMeter()

# Start measurement
meter.start()

# Your workload here
result = expensive_computation()

# Stop and get metrics
metrics = meter.stop()

print(f"Energy consumed: {metrics.energy_joules:.2f} J")
print(f"Duration: {metrics.duration_seconds:.2f} s")
print(f"Average power: {metrics.average_power_watts:.2f} W")
```

### With Context Manager

```python
from greenmining.energy.rapl import RAPLEnergyMeter

meter = RAPLEnergyMeter()

with meter.measure() as measurement:
    # Your analysis code
    analyzer.analyze_repository(repo_url)

print(f"Analysis consumed {measurement.energy_joules:.2f} J")
```

### Permission Setup

RAPL typically requires root access. To allow non-root users:

```bash
# Grant read access to RAPL files
sudo chmod a+r /sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj
sudo chmod a+r /sys/class/powercap/intel-rapl/intel-rapl:0/intel-rapl:0:*/energy_uj

# Or create a udev rule for persistent access
echo 'SUBSYSTEM=="powercap", ACTION=="add", RUN+="/bin/chmod a+r /sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj"' | sudo tee /etc/udev/rules.d/99-rapl.rules
```

---

## CodeCarbon Backend

[CodeCarbon](https://codecarbon.io/) tracks energy consumption and CO2 emissions across platforms.

### Installation

```bash
pip install codecarbon
```

### Basic Usage

```python
from greenmining.energy.codecarbon_meter import CodeCarbonMeter

meter = CodeCarbonMeter(
    country_iso_code="USA",  # For carbon intensity
    project_name="greenmining-analysis",
    tracking_mode="process"  # or "machine"
)

# Start tracking
meter.start()

# Your workload
result = analyzer.analyze_repository(repo_url)

# Stop and get metrics
metrics = meter.stop()

print(f"Energy: {metrics.energy_kwh:.6f} kWh")
print(f"CO2 emissions: {metrics.emissions_kg:.6f} kg")
print(f"Duration: {metrics.duration_seconds:.2f} s")
```

### Configuration Options

```python
meter = CodeCarbonMeter(
    country_iso_code="FRA",      # France
    region="ile-de-france",       # Optional region
    project_name="my-analysis",
    output_dir="./energy_logs",   # Where to save logs
    save_to_file=True,            # Save detailed logs
    tracking_mode="process"       # process or machine
)
```

### Carbon Tracking

```python
from greenmining.energy.codecarbon_meter import CodeCarbonMeter

meter = CodeCarbonMeter(project_name="greenmining")

meter.start()
# ... analysis ...
metrics = meter.stop()

print(f"Energy: {metrics.energy_joules:.2f} J")
print(f"Carbon footprint: {metrics.carbon_grams:.4f} g CO2")
```

---

## Energy Metrics

### EnergyResult Class

```python
from greenmining.energy.base import EnergyResult

@dataclass
class EnergyResult:
    energy_joules: float       # Total energy in Joules
    duration_seconds: float    # Measurement duration
    average_power_watts: float # Average power draw
    start_time: datetime       # Measurement start
    end_time: datetime         # Measurement end
    
    # CodeCarbon specific
    energy_kwh: float = 0.0    # Energy in kilowatt-hours
    emissions_kg: float = 0.0  # CO2 emissions in kg
```

### CommitEnergyProfile

Track energy per commit analysis:

```python
from greenmining.energy.base import CommitEnergyProfile

@dataclass
class CommitEnergyProfile:
    commit_sha: str
    energy_joules: float
    duration_seconds: float
    patterns_detected: list
    files_analyzed: int
```

---

## Research Applications

### Measuring Analysis Efficiency

```python
from greenmining.energy.rapl import RAPLEnergyMeter
from greenmining.services.local_repo_analyzer import LocalRepoAnalyzer

meter = RAPLEnergyMeter()
analyzer = LocalRepoAnalyzer()

repos = [
    "https://github.com/pallets/flask",
    "https://github.com/django/django",
]

results = []
for url in repos:
    meter.start()
    analysis = analyzer.analyze_repository(url, max_commits=100)
    energy = meter.stop()
    
    results.append({
        "repo": url,
        "commits": analysis["total_commits"],
        "energy_joules": energy.energy_joules,
        "joules_per_commit": energy.energy_joules / analysis["total_commits"]
    })

# Compare efficiency
for r in results:
    print(f"{r['repo']}: {r['joules_per_commit']:.3f} J/commit")
```

### Energy-Aware Batch Processing

```python
from greenmining.energy.rapl import RAPLEnergyMeter

meter = RAPLEnergyMeter()
energy_budget_joules = 1000  # Set energy budget

total_energy = 0
analyzed_repos = []

for repo in repositories:
    meter.start()
    result = analyze(repo)
    metrics = meter.stop()
    
    total_energy += metrics.energy_joules
    analyzed_repos.append(repo)
    
    if total_energy >= energy_budget_joules:
        print(f"Energy budget reached after {len(analyzed_repos)} repos")
        break
```

---

## Comparing Backends

| Feature | RAPL | CodeCarbon |
|---------|------|------------|
| **Accuracy** | High (hardware) | Medium (estimation) |
| **Platform** | Linux only | Cross-platform |
| **Granularity** | Microseconds | Seconds |
| **CO2 tracking** | No | Yes |
| **Cloud support** | No | Yes |
| **Setup** | May need root | pip install |

### Recommendation

- Use **RAPL** for precise measurements on Linux
- Use **CodeCarbon** for cross-platform and carbon tracking

---

## Troubleshooting

### RAPL Not Available

```python
# Check if RAPL files exist
import os
rapl_path = "/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj"
print(f"RAPL exists: {os.path.exists(rapl_path)}")

# Check permissions
if os.path.exists(rapl_path):
    print(f"Readable: {os.access(rapl_path, os.R_OK)}")
```

### CodeCarbon Import Error

```bash
# Install with all dependencies
pip install codecarbon[viz]

# Or minimal install
pip install codecarbon
```

### Virtual Machine Limitations

RAPL typically doesn't work in VMs. Use CodeCarbon instead:

```python
from greenmining.energy.rapl import RAPLEnergyMeter
from greenmining.energy.codecarbon_meter import CodeCarbonMeter

# Try RAPL first, fall back to CodeCarbon
rapl = RAPLEnergyMeter()
if rapl.is_available():
    meter = rapl
else:
    print("RAPL not available, using CodeCarbon")
    meter = CodeCarbonMeter()
```

---

## Next Steps

- [Python API](api.md) - Full API reference
- [URL Analysis](url-analysis.md) - Analyze repositories by URL
- [Configuration](../getting-started/configuration.md) - Energy settings
