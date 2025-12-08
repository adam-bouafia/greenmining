"""
Test suite for ML Feature Extractor
"""

import pytest
import tempfile
import os
from datetime import datetime
from greenmining.analyzers.ml_feature_extractor import (
    MLFeatureExtractor,
    MLFeatures
)


class TestMLFeatureExtractor:
    """Test ML feature extraction"""
    
    @pytest.fixture
    def extractor(self):
        """Create feature extractor instance"""
        return MLFeatureExtractor()
    
    @pytest.fixture
    def sample_commit(self):
        """Sample commit"""
        return {
            'hash': 'abc123',
            'message': 'optimize cache performance and reduce memory usage',
            'date': datetime(2024, 6, 15, 14, 30).isoformat(),
            'author_email': 'dev@example.com',
            'repository': 'test-repo',
            'files': [
                {'name': 'cache.py', 'additions': 50, 'deletions': 10},
                {'name': 'memory.py', 'additions': 30, 'deletions': 20},
            ]
        }
    
    @pytest.fixture
    def sample_repository(self):
        """Sample repository"""
        return {
            'name': 'test-repo',
            'stars': 1000,
            'created_at': datetime(2023, 1, 1).isoformat(),
            'language': 'Python'
        }
    
    def test_extract_text_features(self, extractor):
        """Test text feature extraction"""
        text = "optimize cache performance and reduce memory"
        
        features = extractor.extract_text_features(text)
        
        assert 'message_length' in features
        assert 'word_count' in features
        assert 'unique_word_ratio' in features
        assert 'has_green_keywords' in features
        assert 'keyword_count' in features
        assert 'keyword_density' in features
        
        assert features['has_green_keywords'] is True
        assert features['keyword_count'] > 0
        assert features['keyword_density'] > 0
    
    def test_extract_code_metrics(self, extractor, sample_commit):
        """Test code metrics extraction"""
        metrics = extractor.extract_code_metrics(sample_commit)
        
        assert 'files_changed' in metrics
        assert 'lines_added' in metrics
        assert 'lines_deleted' in metrics
        assert 'total_changes' in metrics
        assert 'change_entropy' in metrics
        
        assert metrics['files_changed'] == 2
        assert metrics['lines_added'] == 80
        assert metrics['lines_deleted'] == 30
        assert metrics['total_changes'] == 110
    
    def test_extract_temporal_features(self, extractor, sample_commit):
        """Test temporal feature extraction"""
        all_commits = [sample_commit]
        
        features = extractor.extract_temporal_features(sample_commit, all_commits)
        
        assert 'hour_of_day' in features
        assert 'day_of_week' in features
        assert 'is_weekend' in features
        assert 'commit_velocity' in features
        
        assert 0 <= features['hour_of_day'] <= 23
        assert 0 <= features['day_of_week'] <= 6
        assert isinstance(features['is_weekend'], bool)
    
    def test_extract_repository_features(self, extractor, sample_repository):
        """Test repository feature extraction"""
        features = extractor.extract_repository_features(sample_repository)
        
        assert 'repo_stars' in features
        assert 'repo_age_days' in features
        assert 'primary_language' in features
        
        assert features['repo_stars'] == 1000
        assert features['repo_age_days'] > 0
        assert features['primary_language'] == 'Python'
    
    def test_extract_historical_features(self, extractor, sample_commit):
        """Test historical feature extraction"""
        all_commits = [sample_commit]
        analysis_results = [
            {
                'commit_sha': 'abc123',
                'author_email': 'dev@example.com',
                'repository': 'test-repo',
                'is_green_aware': True
            }
        ]
        
        features = extractor.extract_historical_features(
            sample_commit, all_commits, all_commits, analysis_results
        )
        
        assert 'author_green_rate' in features
        assert 'repo_green_rate' in features
        
        assert 0 <= features['author_green_rate'] <= 1
        assert 0 <= features['repo_green_rate'] <= 1
    
    def test_extract_features_complete(
        self, extractor, sample_commit, sample_repository
    ):
        """Test complete feature extraction"""
        all_commits = [sample_commit]
        analysis_results = [
            {
                'commit_sha': 'abc123',
                'author_email': 'dev@example.com',
                'repository': 'test-repo',
                'is_green_aware': True
            }
        ]
        
        features = extractor.extract_features(
            sample_commit,
            sample_repository,
            all_commits,
            analysis_results,
            ground_truth=True
        )
        
        assert isinstance(features, MLFeatures)
        
        # Text features
        assert features.message_length > 0
        assert features.word_count > 0
        assert features.has_green_keywords is True
        
        # Code features
        assert features.files_changed == 2
        assert features.total_changes == 110
        
        # Temporal features
        assert 0 <= features.hour_of_day <= 23
        
        # Repository features
        assert features.repo_stars == 1000
        assert features.primary_language == 'Python'
        
        # Historical features
        assert 0 <= features.author_green_rate <= 1
        
        # Target label
        assert features.is_green_aware is True
    
    def test_extract_features_batch(
        self, extractor, sample_commit, sample_repository
    ):
        """Test batch feature extraction"""
        commits = [sample_commit, sample_commit]  # Duplicate for testing
        repositories = [sample_repository]
        analysis_results = [
            {
                'commit_sha': 'abc123',
                'author_email': 'dev@example.com',
                'repository': 'test-repo',
                'is_green_aware': True
            }
        ]
        
        features = extractor.extract_features_batch(
            commits, repositories, analysis_results, ground_truth=[True, False]
        )
        
        assert len(features) == 2
        assert all(isinstance(f, MLFeatures) for f in features)
        assert features[0].is_green_aware is True
        assert features[1].is_green_aware is False
    
    def test_export_to_csv(self, extractor, sample_commit, sample_repository):
        """Test CSV export"""
        all_commits = [sample_commit]
        analysis_results = [
            {
                'commit_sha': 'abc123',
                'author_email': 'dev@example.com',
                'repository': 'test-repo',
                'is_green_aware': True
            }
        ]
        
        features = [
            extractor.extract_features(
                sample_commit,
                sample_repository,
                all_commits,
                analysis_results,
                ground_truth=True
            )
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_path = f.name
        
        try:
            extractor.export_to_csv(features, output_path)
            
            # Verify file exists and has content
            assert os.path.exists(output_path)
            
            with open(output_path, 'r') as f:
                lines = f.readlines()
            
            assert len(lines) >= 2  # Header + 1 row
            assert 'message_length' in lines[0]
            assert 'is_green_aware' in lines[0]
        finally:
            os.unlink(output_path)
    
    def test_feature_importance_guide(self, extractor):
        """Test feature importance guide"""
        guide = extractor.get_feature_importance_guide()
        
        assert 'text_features' in guide
        assert 'code_features' in guide
        assert 'temporal_features' in guide
        assert 'repository_features' in guide
        assert 'historical_features' in guide
        
        assert 'keyword_density' in guide['text_features']
        assert 'author_green_rate' in guide['historical_features']
    
    def test_default_keywords(self, extractor):
        """Test default keyword list"""
        keywords = extractor._default_keywords()
        
        assert len(keywords) > 0
        assert 'cache' in keywords
        assert 'optimize' in keywords
        assert 'performance' in keywords
    
    def test_mlfeatures_dataclass(self):
        """Test MLFeatures dataclass"""
        features = MLFeatures(
            message_length=50,
            word_count=10,
            unique_word_ratio=0.8,
            avg_word_length=5.0,
            has_green_keywords=True,
            keyword_count=3,
            keyword_density=0.3,
            files_changed=2,
            lines_added=50,
            lines_deleted=10,
            total_changes=60,
            change_entropy=0.5,
            hour_of_day=14,
            day_of_week=3,
            is_weekend=False,
            commit_velocity=2.5,
            repo_stars=1000,
            repo_age_days=365,
            primary_language='Python',
            author_green_rate=0.75,
            repo_green_rate=0.60,
            is_green_aware=True
        )
        
        assert features.message_length == 50
        assert features.has_green_keywords is True
        assert features.is_green_aware is True
