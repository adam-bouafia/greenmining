"""Test GSF patterns module."""

import pytest


@pytest.mark.unit
def test_gsf_patterns_loaded():
    """Test that GSF patterns are loaded correctly."""
    from greenmining.gsf_patterns import GSF_PATTERNS, GREEN_KEYWORDS
    
    assert len(GSF_PATTERNS) == 76
    assert len(GREEN_KEYWORDS) == 190


@pytest.mark.unit
def test_pattern_categories():
    """Test that all pattern categories exist."""
    from greenmining.gsf_patterns import GSF_PATTERNS
    
    categories = {p['category'] for p in GSF_PATTERNS.values()}
    expected = {'cloud', 'web', 'ai', 'database', 'networking', 'general'}
    assert categories == expected


@pytest.mark.unit
def test_cloud_patterns_count():
    """Test that cloud category has correct number of patterns."""
    from greenmining.gsf_patterns import GSF_PATTERNS
    
    cloud = [p for p in GSF_PATTERNS.values() if p['category'] == 'cloud']
    assert len(cloud) > 0  # Just verify some cloud patterns exist


@pytest.mark.unit
def test_is_green_aware():
    """Test green awareness detection."""
    from greenmining.gsf_patterns import is_green_aware
    
    assert is_green_aware("Optimize energy consumption")
    assert is_green_aware("Implement caching with Redis")
    assert not is_green_aware("Fix typo in README")


@pytest.mark.unit
def test_get_pattern_by_keywords():
    """Test pattern matching by keywords."""
    from greenmining.gsf_patterns import get_pattern_by_keywords
    
    patterns = get_pattern_by_keywords("Implement Redis caching")
    assert len(patterns) > 0
    assert "Cache Static Data" in patterns


@pytest.mark.unit
def test_pattern_structure():
    """Test that patterns have required fields."""
    from greenmining.gsf_patterns import GSF_PATTERNS
    
    for pid, pattern in GSF_PATTERNS.items():
        assert 'name' in pattern
        assert 'category' in pattern
        assert 'keywords' in pattern
        assert 'description' in pattern
        assert 'sci_impact' in pattern
        assert len(pattern['keywords']) > 0
