"""Test data models."""

import pytest


@pytest.mark.unit
def test_repository_model():
    """Test Repository dataclass."""
    from greenmining.models.repository import Repository

    repo = Repository(
        repo_id=123,
        name="test-repo",
        owner="user",
        full_name="user/test-repo",
        url="https://github.com/user/test-repo",
        clone_url="https://github.com/user/test-repo.git",
        language="Python",
        stars=100,
        forks=10,
        watchers=50,
        open_issues=5,
        last_updated="2024-12-01",
        created_at="2024-01-01",
        description="Test repository",
        main_branch="main",
        topics=["test", "example"],
        size=1000,
        has_issues=True,
        has_wiki=True,
        archived=False,
        license="MIT",
    )

    assert repo.name == "test-repo"
    assert repo.stars == 100
    assert repo.language == "Python"


@pytest.mark.unit
def test_commit_model():
    """Test Commit dataclass."""
    from greenmining.models.commit import Commit

    commit = Commit(
        commit_id="abc123",
        repo_name="test-repo",
        date="2024-12-01",
        author="Test Author",
        author_email="test@example.com",
        message="Test commit message",
        files_changed=["file1.py", "file2.py"],
        lines_added=10,
        lines_deleted=5,
        insertions=10,
        deletions=5,
        is_merge=False,
        branches=["main"],
        in_main_branch=True,
    )

    assert commit.commit_id == "abc123"
    assert commit.author == "Test Author"
    assert commit.insertions == 10


@pytest.mark.unit
def test_analysis_result_model():
    """Test AnalysisResult dataclass."""
    from greenmining.models.analysis_result import AnalysisResult

    result = AnalysisResult(
        commit_id="abc123",
        repo_name="test-repo",
        date="2024-12-01",
        commit_message="Implement Redis caching",
        green_aware=True,
        green_evidence="cache, redis",
        known_pattern="Cache Static Data",
        pattern_confidence="high",
        emergent_pattern=None,
        files_changed=["cache.py"],
        lines_added=10,
        lines_deleted=2,
    )

    assert result.green_aware is True
    assert result.known_pattern == "Cache Static Data"
    assert result.pattern_confidence == "high"
