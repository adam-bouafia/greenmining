"""
Test suite for Temporal Analyzer
"""

import pytest
from datetime import datetime, timedelta
from greenmining.analyzers.temporal_analyzer import (
    TemporalAnalyzer,
    TemporalMetrics,
    TrendAnalysis
)


class TestTemporalAnalyzer:
    """Test temporal and historical analysis"""
    
    @pytest.fixture
    def analyzer(self):
        """Create temporal analyzer instance"""
        return TemporalAnalyzer(granularity='quarter')
    
    @pytest.fixture
    def sample_commits(self):
        """Sample commits with dates"""
        base_date = datetime(2024, 1, 1)
        commits = []
        
        for i in range(12):  # 12 months
            date = base_date + timedelta(days=i * 30)
            commits.append({
                'hash': f'commit{i}',
                'date': date.isoformat(),
                'message': 'test commit',
                'repository': 'test-repo'
            })
        
        return commits
    
    @pytest.fixture
    def sample_analysis_results(self):
        """Sample analysis results"""
        results = []
        
        # First 6 commits are green (50% rate)
        for i in range(12):
            results.append({
                'commit_sha': f'commit{i}',
                'is_green_aware': i < 6,
                'patterns_detected': ['caching'] if i < 6 else [],
                'commit_date': datetime(2024, 1 + i, 1).isoformat()
            })
        
        return results
    
    def test_group_commits_by_quarter(self, analyzer, sample_commits):
        """Test grouping commits by quarter"""
        grouped = analyzer.group_commits_by_period(sample_commits)
        
        assert len(grouped) > 0
        assert '2024-Q1' in grouped or '2024-Q2' in grouped
    
    def test_group_commits_by_month(self, sample_commits):
        """Test grouping by month"""
        analyzer = TemporalAnalyzer(granularity='month')
        grouped = analyzer.group_commits_by_period(sample_commits)
        
        assert len(grouped) >= 10  # Should have multiple months
        assert '2024-01' in grouped or '2024-02' in grouped
    
    def test_calculate_period_metrics(self, analyzer, sample_commits, sample_analysis_results):
        """Test metrics calculation for a period"""
        grouped = analyzer.group_commits_by_period(sample_commits)
        period_key = list(grouped.keys())[0]
        
        metrics = analyzer.calculate_period_metrics(
            period_key,
            grouped[period_key],
            sample_analysis_results
        )
        
        assert isinstance(metrics, TemporalMetrics)
        assert metrics.commit_count > 0
        assert metrics.green_awareness_rate >= 0
        assert metrics.velocity >= 0
    
    def test_analyze_trends(self, analyzer, sample_commits, sample_analysis_results):
        """Test comprehensive trend analysis"""
        analysis = analyzer.analyze_trends(sample_commits, sample_analysis_results)
        
        assert 'periods' in analysis
        assert 'trend' in analysis
        assert 'adoption_curve' in analysis
        assert 'velocity_trend' in analysis
        assert 'pattern_evolution' in analysis
        assert 'summary' in analysis
        
        assert len(analysis['periods']) > 0
    
    def test_trend_calculation(self, analyzer):
        """Test trend direction calculation"""
        # Create increasing trend
        periods = [
            TemporalMetrics(
                period=f'2024-Q{i}',
                start_date=datetime(2024, 1 + (i-1)*3, 1),
                end_date=datetime(2024, min(12, 3 + (i-1)*3), 28),
                commit_count=10,
                green_commit_count=i * 2,
                green_awareness_rate=i * 20.0,
                unique_patterns=3,
                dominant_pattern='caching',
                velocity=0.5
            )
            for i in range(1, 5)
        ]
        
        trend = analyzer._calculate_trend(periods)
        
        assert trend is not None
        assert trend.trend_direction in ['increasing', 'stable', 'decreasing']
        assert trend.slope != 0  # Should have positive slope
    
    def test_adoption_curve(self, analyzer):
        """Test cumulative adoption curve calculation"""
        periods = [
            TemporalMetrics(
                period=f'2024-Q{i}',
                start_date=datetime(2024, 1 + (i-1)*3, 1),
                end_date=datetime(2024, min(12, 3 + (i-1)*3), 28),
                commit_count=10,
                green_commit_count=i * 2,
                green_awareness_rate=i * 20.0,
                unique_patterns=3,
                dominant_pattern='caching',
                velocity=0.5
            )
            for i in range(1, 5)
        ]
        
        curve = analyzer._calculate_adoption_curve(periods)
        
        assert len(curve) == len(periods)
        assert all(isinstance(point, tuple) for point in curve)
        assert all(point[1] >= 0 for point in curve)  # Rates should be non-negative
    
    def test_velocity_trend(self, analyzer):
        """Test velocity trend calculation"""
        periods = [
            TemporalMetrics(
                period=f'2024-Q{i}',
                start_date=datetime(2024, 1 + (i-1)*3, 1),
                end_date=datetime(2024, min(12, 3 + (i-1)*3), 28),
                commit_count=10,
                green_commit_count=5,
                green_awareness_rate=50.0,
                unique_patterns=3,
                dominant_pattern='caching',
                velocity=i * 0.5  # Increasing velocity
            )
            for i in range(1, 5)
        ]
        
        velocity_trend = analyzer._calculate_velocity_trend(periods)
        
        assert 'average_velocity' in velocity_trend
        assert 'velocity_std' in velocity_trend
        assert 'min_velocity' in velocity_trend
        assert 'max_velocity' in velocity_trend
        assert velocity_trend['max_velocity'] > velocity_trend['min_velocity']
    
    def test_parse_period_key_quarter(self, analyzer):
        """Test parsing quarter period keys"""
        start, end = analyzer._parse_period_key('2024-Q1')
        
        assert start.year == 2024
        assert start.month == 1
        assert end.month in [3, 4]  # End of Q1
    
    def test_parse_period_key_month(self, analyzer):
        """Test parsing month period keys"""
        start, end = analyzer._parse_period_key('2024-06')
        
        assert start.year == 2024
        assert start.month == 6
        assert end.month in [6, 7]
    
    def test_parse_period_key_year(self, analyzer):
        """Test parsing year period keys"""
        start, end = analyzer._parse_period_key('2024')
        
        assert start.year == 2024
        assert start.month == 1
        assert end.year == 2024
        assert end.month == 12
    
    def test_pattern_evolution(self, analyzer, sample_commits, sample_analysis_results):
        """Test pattern evolution tracking"""
        grouped = analyzer.group_commits_by_period(sample_commits)
        periods = []
        
        for period_key in sorted(grouped.keys()):
            metrics = analyzer.calculate_period_metrics(
                period_key,
                grouped[period_key],
                sample_analysis_results
            )
            periods.append(metrics)
        
        evolution = analyzer._analyze_pattern_evolution(periods, sample_analysis_results)
        
        assert isinstance(evolution, dict)
        # Should have pattern entries if green commits exist
        if any(r['is_green_aware'] for r in sample_analysis_results):
            assert len(evolution) > 0
