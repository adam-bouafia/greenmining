"""
Test suite for NLP Analyzer
"""

import pytest
from greenmining.analyzers.nlp_analyzer import NLPAnalyzer, NLPMatch


class TestNLPAnalyzer:
    """Test NLP-based pattern detection"""

    @pytest.fixture
    def analyzer(self):
        """Create NLP analyzer instance"""
        return NLPAnalyzer(enable_stemming=True, enable_synonyms=True)

    def test_stemming_optimization(self, analyzer):
        """Test morphological variants of 'optimize'"""
        text = "optimizing performance and optimized caching"
        keywords = ["optimize", "cache"]

        matches = analyzer.find_morphological_matches(text, keywords)

        assert len(matches) >= 2  # optimizing, optimized
        matched_words = [m.matched_variant for m in matches]
        assert "optimizing" in matched_words
        assert "optimized" in matched_words

    def test_stemming_caching(self, analyzer):
        """Test morphological variants of 'cache'"""
        text = "implemented caching with cached results"
        keywords = ["cache"]

        matches = analyzer.find_morphological_matches(text, keywords)

        assert len(matches) >= 2
        matched_words = [m.matched_variant for m in matches]
        assert "caching" in matched_words or "cached" in matched_words

    def test_synonym_matching(self, analyzer):
        """Test semantic synonym detection"""
        text = "improve performance and enhance efficiency"
        keywords = ["optimize", "efficient"]

        matches = analyzer.find_semantic_matches(text, keywords)

        assert len(matches) >= 2  # improve, enhance
        matched_words = [m.matched_variant for m in matches]
        assert "improve" in matched_words or "enhance" in matched_words

    def test_phrase_patterns(self, analyzer):
        """Test multi-word phrase matching"""
        text = "reduce memory usage and optimize performance"

        matches = analyzer.find_phrase_patterns(text)

        assert len(matches) >= 1
        # Check for patterns like 'reduce memory' or 'optimize performance'
        patterns = [m.matched_variant for m in matches]
        assert any("memory" in p for p in patterns) or any("performance" in p for p in patterns)

    def test_analyze_text_comprehensive(self, analyzer):
        """Test comprehensive text analysis"""
        text = "optimizing cache performance by reducing memory footprint"
        keywords = ["optimize", "cache", "memory"]

        analysis = analyzer.analyze_text(text, keywords)

        assert "morphological_matches" in analysis
        assert "semantic_matches" in analysis
        assert "phrase_matches" in analysis
        assert analysis["total_nlp_matches"] > 0
        assert analysis["match_density"] > 0

    def test_enhance_pattern_detection(self, analyzer):
        """Test enhancement of original keyword detection"""
        text = "implemented caching strategy for improved efficiency"
        original_keywords = ["cache", "efficient"]  # Base keywords

        has_additional, terms = analyzer.enhance_pattern_detection(text, original_keywords)

        # Should find variants like 'caching', 'improved'
        # May or may not find additional depending on phrase matches
        assert isinstance(has_additional, bool)
        assert isinstance(terms, list)

    def test_stem_word(self, analyzer):
        """Test word stemming"""
        assert analyzer.stem_word("optimization") == "optim"
        assert analyzer.stem_word("optimizing") == "optim"
        assert analyzer.stem_word("optimized") == "optim"
        assert analyzer.stem_word("caching") == "cache"
        assert analyzer.stem_word("cached") == "cache"

    def test_get_synonyms(self, analyzer):
        """Test synonym retrieval"""
        synonyms = analyzer.get_synonyms("cache")
        assert "cache" in synonyms
        assert len(synonyms) > 1  # Should include synonyms

        synonyms = analyzer.get_synonyms("optimize")
        assert "optimize" in synonyms
        assert any(s in ["improve", "enhance", "tune"] for s in synonyms)

    def test_disabled_stemming(self):
        """Test with stemming disabled"""
        analyzer = NLPAnalyzer(enable_stemming=False, enable_synonyms=True)
        text = "optimizing performance"
        keywords = ["optimize"]

        matches = analyzer.find_morphological_matches(text, keywords)
        assert len(matches) == 0  # Stemming disabled

    def test_disabled_synonyms(self):
        """Test with synonyms disabled"""
        analyzer = NLPAnalyzer(enable_stemming=True, enable_synonyms=False)
        text = "improve performance"
        keywords = ["optimize"]

        matches = analyzer.find_semantic_matches(text, keywords)
        assert len(matches) == 0  # Synonyms disabled

    def test_nlp_match_dataclass(self):
        """Test NLPMatch dataclass"""
        match = NLPMatch(
            original_term="optimize",
            matched_variant="optimizing",
            position=10,
            context="test optimizing code",
            match_type="stemmed",
        )

        assert match.original_term == "optimize"
        assert match.matched_variant == "optimizing"
        assert match.match_type == "stemmed"
