#!/usr/bin/env python3
"""
Generate publication-quality plots for the GreenMining thesis.
Creates figures from aggregated_statistics.json and analysis_results.json.
"""

import json
import os
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Set publication-quality defaults
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (8, 5),
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "thesis" / "figures"

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load all data files."""
    with open(DATA_DIR / "aggregated_statistics.json") as f:
        stats = json.load(f)
    with open(DATA_DIR / "analysis_results.json") as f:
        results = json.load(f)
    return stats, results


def plot_pattern_frequency(stats, output_path):
    """
    Figure 1: Horizontal bar chart of top 15 patterns by frequency.
    """
    patterns = stats.get("known_patterns", [])
    
    # Get top 15 patterns
    top_patterns = sorted(patterns, key=lambda x: x["count"], reverse=True)[:15]
    
    names = [p["pattern_name"] for p in top_patterns]
    counts = [p["count"] for p in top_patterns]
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Create horizontal bar chart
    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, counts, color='#2E86AB', edgecolor='#1B4F72', linewidth=0.5)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.invert_yaxis()  # Top pattern at top
    ax.set_xlabel('Number of Matches')
    ax.set_title('Top 15 Most Frequently Detected Green Software Patterns')
    
    # Add count labels on bars
    for i, (bar, count) in enumerate(zip(bars, counts)):
        ax.text(count + 0.5, bar.get_y() + bar.get_height()/2, 
                str(count), va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def plot_category_distribution(stats, results, output_path):
    """
    Figure 2: Bar chart showing pattern matches by category.
    """
    # Count patterns by category from results
    category_counts = defaultdict(int)
    
    for commit in results:
        if commit.get("green_aware"):
            for detail in commit.get("pattern_details", []):
                category = detail.get("category", "unknown")
                category_counts[category] += 1
    
    # Sort by count
    sorted_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    categories = [c[0].title() for c in sorted_cats]
    counts = [c[1] for c in sorted_cats]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Color palette
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(categories)))
    
    bars = ax.bar(categories, counts, color=colors, edgecolor='#1B4F72', linewidth=0.5)
    
    ax.set_xlabel('Pattern Category')
    ax.set_ylabel('Number of Pattern Matches')
    ax.set_title('Distribution of Green Software Patterns by Category')
    
    # Rotate x labels
    plt.xticks(rotation=45, ha='right')
    
    # Add count labels
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                str(count), ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def plot_confidence_distribution(stats, output_path):
    """
    Figure 3: Stacked bar chart showing confidence levels for top patterns.
    """
    patterns = stats.get("known_patterns", [])
    top_patterns = sorted(patterns, key=lambda x: x["count"], reverse=True)[:10]
    
    names = [p["pattern_name"][:25] + "..." if len(p["pattern_name"]) > 25 
             else p["pattern_name"] for p in top_patterns]
    
    high = [p["confidence_breakdown"].get("HIGH", 0) for p in top_patterns]
    medium = [p["confidence_breakdown"].get("MEDIUM", 0) for p in top_patterns]
    low = [p["confidence_breakdown"].get("LOW", 0) for p in top_patterns]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(names))
    width = 0.6
    
    ax.bar(x, high, width, label='High Confidence', color='#27AE60', edgecolor='white')
    ax.bar(x, medium, width, bottom=high, label='Medium Confidence', color='#F39C12', edgecolor='white')
    ax.bar(x, low, width, bottom=np.array(high)+np.array(medium), 
           label='Low Confidence', color='#E74C3C', edgecolor='white')
    
    ax.set_xlabel('Pattern')
    ax.set_ylabel('Number of Matches')
    ax.set_title('Confidence Level Distribution for Top 10 Patterns')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def plot_repository_comparison(results, output_path):
    """
    Figure 4: Bar chart comparing green awareness across repositories.
    """
    # Group by repository
    repo_stats = defaultdict(lambda: {"total": 0, "green": 0})
    
    for commit in results:
        repo = commit.get("repository", "unknown")
        repo_stats[repo]["total"] += 1
        if commit.get("green_aware"):
            repo_stats[repo]["green"] += 1
    
    # Calculate percentages and sort
    repo_data = []
    for repo, data in repo_stats.items():
        if data["total"] > 0:
            pct = (data["green"] / data["total"]) * 100
            repo_data.append((repo.split("/")[-1], pct, data["green"], data["total"]))
    
    repo_data.sort(key=lambda x: x[1], reverse=True)
    
    # Take top 10
    top_repos = repo_data[:10]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    names = [r[0] for r in top_repos]
    pcts = [r[1] for r in top_repos]
    
    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(names)))
    bars = ax.bar(names, pcts, color=colors, edgecolor='#1B4F72', linewidth=0.5)
    
    ax.set_xlabel('Repository')
    ax.set_ylabel('Green-Aware Commits (%)')
    ax.set_title('Green Software Awareness by Repository (Top 10)')
    ax.set_ylim(0, 100)
    
    plt.xticks(rotation=45, ha='right')
    
    # Add percentage labels
    for bar, pct in zip(bars, pcts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def plot_green_awareness_boxplot(results, output_path):
    """
    Figure 5: Box plot showing distribution of green awareness rates.
    """
    # Group by repository
    repo_stats = defaultdict(lambda: {"total": 0, "green": 0})
    
    for commit in results:
        repo = commit.get("repository", "unknown")
        repo_stats[repo]["total"] += 1
        if commit.get("green_aware"):
            repo_stats[repo]["green"] += 1
    
    # Calculate percentages
    percentages = []
    for repo, data in repo_stats.items():
        if data["total"] > 0:
            pct = (data["green"] / data["total"]) * 100
            percentages.append(pct)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    bp = ax.boxplot(percentages, patch_artist=True, widths=0.5)
    
    # Style the boxplot
    bp['boxes'][0].set_facecolor('#3498DB')
    bp['boxes'][0].set_alpha(0.7)
    bp['medians'][0].set_color('#E74C3C')
    bp['medians'][0].set_linewidth(2)
    
    ax.set_ylabel('Green-Aware Commits (%)')
    ax.set_title('Distribution of Green Software Awareness Across Repositories')
    ax.set_xticklabels(['All Repositories'])
    
    # Add statistics annotation
    median = np.median(percentages)
    mean = np.mean(percentages)
    std = np.std(percentages)
    
    stats_text = f'Mean: {mean:.1f}%\nMedian: {median:.1f}%\nStd: {std:.1f}%\nn = {len(percentages)} repos'
    ax.text(0.98, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def plot_pattern_cooccurrence(results, output_path):
    """
    Figure 6: Heatmap showing pattern co-occurrence.
    """
    # Get top 8 patterns for readability
    pattern_counts = Counter()
    for commit in results:
        for pattern in commit.get("gsf_patterns_matched", []):
            pattern_counts[pattern] += 1
    
    top_patterns = [p[0] for p in pattern_counts.most_common(8)]
    
    # Build co-occurrence matrix
    cooccurrence = np.zeros((len(top_patterns), len(top_patterns)))
    
    for commit in results:
        matched = commit.get("gsf_patterns_matched", [])
        for i, p1 in enumerate(top_patterns):
            for j, p2 in enumerate(top_patterns):
                if p1 in matched and p2 in matched:
                    cooccurrence[i][j] += 1
    
    # Normalize by diagonal (self-occurrence)
    for i in range(len(top_patterns)):
        if cooccurrence[i][i] > 0:
            cooccurrence[i] = cooccurrence[i] / cooccurrence[i][i]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Shorten names
    short_names = [p[:20] + "..." if len(p) > 20 else p for p in top_patterns]
    
    im = ax.imshow(cooccurrence, cmap='YlGnBu', aspect='auto')
    
    ax.set_xticks(np.arange(len(short_names)))
    ax.set_yticks(np.arange(len(short_names)))
    ax.set_xticklabels(short_names, rotation=45, ha='right')
    ax.set_yticklabels(short_names)
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Normalized Co-occurrence', rotation=-90, va='bottom')
    
    ax.set_title('Pattern Co-occurrence Matrix (Top 8 Patterns)')
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def plot_summary_statistics(stats, results, output_path):
    """
    Figure 7: Summary statistics infographic-style figure.
    """
    summary = stats.get("summary", {})
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    
    # Plot 1: Green awareness pie chart
    ax1 = axes[0, 0]
    green_pct = summary.get("green_aware_percentage", 0)
    sizes = [green_pct, 100 - green_pct]
    colors = ['#27AE60', '#BDC3C7']
    explode = (0.05, 0)
    ax1.pie(sizes, explode=explode, colors=colors, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.set_title('Green-Aware vs Non-Green Commits')
    
    # Legend
    green_patch = mpatches.Patch(color='#27AE60', label='Green-aware')
    other_patch = mpatches.Patch(color='#BDC3C7', label='Not green-aware')
    ax1.legend(handles=[green_patch, other_patch], loc='lower right')
    
    # Plot 2: Repository coverage
    ax2 = axes[0, 1]
    repos_with_green = summary.get("repos_with_green_commits", 0)
    total_repos = summary.get("total_repos", 1)
    ax2.bar(['With Green\nCommits', 'Without Green\nCommits'], 
            [repos_with_green, total_repos - repos_with_green],
            color=['#27AE60', '#BDC3C7'])
    ax2.set_ylabel('Number of Repositories')
    ax2.set_title('Repository Coverage')
    
    # Plot 3: Commits analyzed
    ax3 = axes[1, 0]
    total = summary.get("total_commits", 0)
    green = summary.get("green_aware_count", 0)
    ax3.bar(['Total Commits', 'Green-Aware'], [total, green], 
            color=['#3498DB', '#27AE60'])
    ax3.set_ylabel('Count')
    ax3.set_title('Commit Analysis Summary')
    
    # Add labels
    for i, v in enumerate([total, green]):
        ax3.text(i, v + 2, str(v), ha='center', fontsize=10)
    
    # Plot 4: Pattern category breakdown (top 5)
    ax4 = axes[1, 1]
    patterns = stats.get("known_patterns", [])
    
    # Group by inferred category from pattern names
    category_counts = defaultdict(int)
    for p in patterns:
        # Simple category inference from name
        name = p["pattern_name"].lower()
        if "cache" in name:
            category_counts["Caching"] += p["count"]
        elif "request" in name or "api" in name:
            category_counts["Network/API"] += p["count"]
        elif "cloud" in name or "kubernetes" in name or "container" in name:
            category_counts["Cloud/Infra"] += p["count"]
        elif "data" in name or "storage" in name:
            category_counts["Data/Storage"] += p["count"]
        else:
            category_counts["Other"] += p["count"]
    
    sorted_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    cat_names = [c[0] for c in sorted_cats]
    cat_counts = [c[1] for c in sorted_cats]
    
    ax4.barh(cat_names, cat_counts, color=plt.cm.Greens(np.linspace(0.3, 0.9, len(cat_names))))
    ax4.set_xlabel('Pattern Matches')
    ax4.set_title('Top Pattern Categories')
    ax4.invert_yaxis()
    
    plt.suptitle('GreenMining Analysis Summary', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def main():
    """Generate all thesis plots."""
    print("Loading data...")
    stats, results = load_data()
    
    print(f"\nData loaded:")
    print(f"  - Total commits: {stats['summary']['total_commits']}")
    print(f"  - Green-aware: {stats['summary']['green_aware_count']} ({stats['summary']['green_aware_percentage']:.1f}%)")
    print(f"  - Patterns tracked: {len(stats.get('known_patterns', []))}")
    
    print(f"\nGenerating plots in {OUTPUT_DIR}...")
    
    # Generate all figures
    plot_pattern_frequency(stats, OUTPUT_DIR / "fig_pattern_frequency.pdf")
    plot_category_distribution(stats, results, OUTPUT_DIR / "fig_category_distribution.pdf")
    plot_confidence_distribution(stats, OUTPUT_DIR / "fig_confidence_levels.pdf")
    plot_repository_comparison(results, OUTPUT_DIR / "fig_repository_comparison.pdf")
    plot_green_awareness_boxplot(results, OUTPUT_DIR / "fig_awareness_boxplot.pdf")
    plot_pattern_cooccurrence(results, OUTPUT_DIR / "fig_pattern_cooccurrence.pdf")
    plot_summary_statistics(stats, results, OUTPUT_DIR / "fig_summary_statistics.pdf")
    
    print("\nAll plots generated successfully!")
    print(f"\nTo include in LaTeX, add to your preamble:")
    print("  \\usepackage{graphicx}")
    print("  \\graphicspath{{figures/}}")
    print("\nThen use:")
    print("  \\includegraphics[width=\\textwidth]{fig_pattern_frequency}")


if __name__ == "__main__":
    main()
