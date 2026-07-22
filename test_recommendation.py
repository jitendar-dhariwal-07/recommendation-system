"""
Unit Tests for Recommendation System

Tests for similarity calculations, recommendation algorithms, and edge cases.
Run with: pytest test_recommendation.py -v
"""

import pytest
from recommendation_engine import (
    SimilarityCalculator, RecommendationEngine, SimilarityMetric, User, Item
)
from data_manager import DataManager
from typing import Dict


class TestSimilarityCalculator:
    """Tests for similarity calculation metrics."""

    def test_euclidean_distance_identical_vectors(self):
        """Identical vectors should have 0 distance."""
        vec1 = {"a": 1, "b": 2, "c": 3}
        vec2 = {"a": 1, "b": 2, "c": 3}
        
        distance = SimilarityCalculator.euclidean_distance(vec1, vec2)
        assert distance == pytest.approx(0.0)

    def test_euclidean_distance_different_vectors(self):
        """Test distance calculation between different vectors."""
        vec1 = {"a": 0, "b": 0}
        vec2 = {"a": 3, "b": 4}
        
        distance = SimilarityCalculator.euclidean_distance(vec1, vec2)
        assert distance == pytest.approx(5.0)  # 3-4-5 triangle

    def test_euclidean_similarity_scale(self):
        """Euclidean similarity should be in range [0, 1]."""
        vec1 = {"a": 1, "b": 2}
        vec2 = {"a": 10, "b": 20}
        
        similarity = SimilarityCalculator.euclidean_similarity(vec1, vec2)
        assert 0 <= similarity <= 1

    def test_cosine_similarity_identical(self):
        """Identical vectors should have similarity 1."""
        vec1 = {"a": 1, "b": 2, "c": 3}
        vec2 = {"a": 1, "b": 2, "c": 3}
        
        similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
        assert similarity == pytest.approx(1.0)

    def test_cosine_similarity_orthogonal(self):
        """Orthogonal vectors should have similarity 0."""
        vec1 = {"a": 1, "b": 0}
        vec2 = {"a": 0, "b": 1}
        
        similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
        assert similarity == pytest.approx(0.0)

    def test_cosine_similarity_partial_overlap(self):
        """Test similarity with partial feature overlap."""
        vec1 = {"a": 1, "b": 2}
        vec2 = {"a": 2, "c": 3}  # Only 'a' overlaps
        
        # Should only consider overlapping features
        similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
        assert similarity > 0
        assert similarity <= 1

    def test_cosine_similarity_empty_vectors(self):
        """Empty vectors should return 0."""
        vec1 = {}
        vec2 = {}
        
        similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
        assert similarity == 0.0

    def test_jaccard_similarity_identical_sets(self):
        """Identical sets should have similarity 1."""
        set1 = {"a", "b", "c"}
        set2 = {"a", "b", "c"}
        
        similarity = SimilarityCalculator.jaccard_similarity(set1, set2)
        assert similarity == pytest.approx(1.0)

    def test_jaccard_similarity_disjoint(self):
        """Disjoint sets should have similarity 0."""
        set1 = {"a", "b"}
        set2 = {"c", "d"}
        
        similarity = SimilarityCalculator.jaccard_similarity(set1, set2)
        assert similarity == pytest.approx(0.0)

    def test_jaccard_similarity_partial_overlap(self):
        """Test similarity with partial overlap."""
        set1 = {"a", "b", "c"}
        set2 = {"b", "c", "d"}
        
        # Intersection: {b, c}, Union: {a, b, c, d}
        # Similarity = 2/4 = 0.5
        similarity = SimilarityCalculator.jaccard_similarity(set1, set2)
        assert similarity == pytest.approx(0.5)

    def test_jaccard_similarity_empty_sets(self):
        """Empty sets should have similarity 1."""
        set1 = set()
        set2 = set()
        
        similarity = SimilarityCalculator.jaccard_similarity(set1, set2)
        assert similarity == 1.0


class TestRecommendationEngine:
    """Tests for recommendation algorithms."""

    @pytest.fixture
    def engine(self):
        """Create a recommendation engine."""
        return RecommendationEngine(metric=SimilarityMetric.COSINE)

    @pytest.fixture
    def sample_users(self):
        """Get sample users."""
        return DataManager.get_sample_users()

    @pytest.fixture
    def sample_items(self):
        """Get sample items."""
        return DataManager.get_sample_books()

    def test_content_based_returns_correct_type(self, engine, sample_users, sample_items):
        """Content-based recommendations should return list of tuples."""
        user = sample_users[0]
        recs = engine.content_based_recommendations(user, sample_items, top_n=3)
        
        assert isinstance(recs, list)
        assert len(recs) <= 3
        assert all(isinstance(item, Item) and isinstance(score, float) for item, score in recs)

    def test_content_based_scores_positive(self, engine, sample_users, sample_items):
        """All recommendation scores should be non-negative."""
        user = sample_users[0]
        recs = engine.content_based_recommendations(user, sample_items, top_n=5)
        
        assert all(score >= 0 for _, score in recs)

    def test_content_based_exclude_liked(self, engine, sample_users, sample_items):
        """Exclude liked items should work correctly."""
        user = sample_users[0]
        
        # Get recommendations excluding liked items
        recs_excluded = engine.content_based_recommendations(
            user, sample_items, top_n=10, exclude_liked=True
        )
        
        # Check no liked items are in recommendations
        rec_item_ids = {item.item_id for item, _ in recs_excluded}
        assert not rec_item_ids.intersection(user.liked_items)

    def test_content_based_sorted_by_score(self, engine, sample_users, sample_items):
        """Recommendations should be sorted by score (descending)."""
        user = sample_users[0]
        recs = engine.content_based_recommendations(user, sample_items, top_n=5)
        
        scores = [score for _, score in recs]
        assert scores == sorted(scores, reverse=True)

    def test_content_based_respects_top_n(self, engine, sample_users, sample_items):
        """Should return at most top_n recommendations."""
        user = sample_users[0]
        
        for n in [1, 3, 5, 10]:
            recs = engine.content_based_recommendations(user, sample_items, top_n=n)
            assert len(recs) <= n

    def test_collaborative_filtering_returns_list(self, engine, sample_users, sample_items):
        """Collaborative filtering should return list of tuples."""
        user = sample_users[0]
        recs = engine.collaborative_filtering_recommendations(
            user, sample_users, sample_items, top_n=3
        )
        
        assert isinstance(recs, list)
        assert all(isinstance(item, Item) and isinstance(score, float) for item, score in recs)

    def test_collaborative_filtering_skips_user(self, engine, sample_users, sample_items):
        """Shouldn't recommend items target user already liked."""
        user = sample_users[0]
        recs = engine.collaborative_filtering_recommendations(
            user, sample_users, sample_items, top_n=10
        )
        
        rec_item_ids = {item.item_id for item, _ in recs}
        assert not rec_item_ids.intersection(user.liked_items)

    def test_collaborative_filtering_with_k_neighbors(self, engine, sample_users, sample_items):
        """Test collaborative filtering with different k values."""
        user = sample_users[0]
        
        recs_k1 = engine.collaborative_filtering_recommendations(
            user, sample_users, sample_items, top_n=5, k_neighbors=1
        )
        
        recs_k3 = engine.collaborative_filtering_recommendations(
            user, sample_users, sample_items, top_n=5, k_neighbors=3
        )
        
        # Both should return lists (may be different lengths/content)
        assert isinstance(recs_k1, list)
        assert isinstance(recs_k3, list)

    def test_hybrid_recommendations_combines_scores(self, engine, sample_users, sample_items):
        """Hybrid recommendations should combine multiple approaches."""
        user = sample_users[0]
        
        recs = engine.hybrid_recommendations(
            user, sample_users, sample_items, top_n=5,
            content_weight=0.6, collaborative_weight=0.4
        )
        
        assert isinstance(recs, list)
        assert all(isinstance(item, Item) and isinstance(score, float) for item, score in recs)

    def test_hybrid_recommendations_weight_variations(self, engine, sample_users, sample_items):
        """Test hybrid recommendations with different weight combinations."""
        user = sample_users[0]
        
        # All content-based
        recs_content = engine.hybrid_recommendations(
            user, sample_users, sample_items, top_n=5,
            content_weight=1.0, collaborative_weight=0.0
        )
        
        # All collaborative
        recs_collab = engine.hybrid_recommendations(
            user, sample_users, sample_items, top_n=5,
            content_weight=0.0, collaborative_weight=1.0
        )
        
        # Results may differ based on weights
        assert isinstance(recs_content, list)
        assert isinstance(recs_collab, list)

    def test_category_filtered_recommendations(self, engine, sample_users):
        """Test category-filtered recommendations."""
        user = sample_users[0]
        items = DataManager.get_all_items()
        
        recs = engine.category_filtered_recommendations(
            user, items, categories=["Technology"], top_n=5
        )
        
        # All recommendations should be from Technology category
        assert all(item.category == "Technology" for item, _ in recs)

    def test_empty_items_list(self, engine, sample_users):
        """Handle empty items list gracefully."""
        user = sample_users[0]
        recs = engine.content_based_recommendations(user, [], top_n=5)
        
        assert recs == []

    def test_single_item(self, engine, sample_users, sample_items):
        """Handle single item correctly."""
        user = sample_users[0]
        single_item = [sample_items[0]]
        
        recs = engine.content_based_recommendations(user, single_item, top_n=5)
        
        assert len(recs) <= 1

    def test_similarity_metric_selection(self, sample_users, sample_items):
        """Different metrics should be supported."""
        user = sample_users[0]
        
        for metric in [SimilarityMetric.COSINE, SimilarityMetric.EUCLIDEAN, SimilarityMetric.JACCARD]:
            engine = RecommendationEngine(metric=metric)
            recs = engine.content_based_recommendations(user, sample_items, top_n=3)
            
            assert isinstance(recs, list)
            assert len(recs) <= 3


class TestDataManager:
    """Tests for data manager."""

    def test_sample_data_loaded(self):
        """Sample data should load correctly."""
        books = DataManager.get_sample_books()
        movies = DataManager.get_sample_movies()
        courses = DataManager.get_sample_courses()
        users = DataManager.get_sample_users()
        
        assert len(books) > 0
        assert len(movies) > 0
        assert len(courses) > 0
        assert len(users) > 0

    def test_all_items_combined(self):
        """All items should combine correctly."""
        all_items = DataManager.get_all_items()
        books = DataManager.get_sample_books()
        movies = DataManager.get_sample_movies()
        courses = DataManager.get_sample_courses()
        
        expected_count = len(books) + len(movies) + len(courses)
        assert len(all_items) == expected_count

    def test_item_structure(self):
        """Items should have required structure."""
        items = DataManager.get_all_items()
        
        for item in items:
            assert isinstance(item.item_id, str)
            assert isinstance(item.name, str)
            assert isinstance(item.description, str)
            assert isinstance(item.features, dict)
            assert isinstance(item.category, str)
            assert isinstance(item.tags, set)

    def test_user_structure(self):
        """Users should have required structure."""
        users = DataManager.get_sample_users()
        
        for user in users:
            assert isinstance(user.user_id, str)
            assert isinstance(user.name, str)
            assert isinstance(user.preferences, dict)
            assert isinstance(user.liked_items, set)


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_zero_preferences(self):
        """Handle user with all zero preferences."""
        user = User(
            user_id="test_001",
            name="Test User",
            preferences={"a": 0, "b": 0, "c": 0},
            liked_items=set()
        )
        
        item = Item(
            item_id="test_item",
            name="Test Item",
            description="Test",
            features={"a": 1, "b": 1, "c": 1},
            category="Test",
            tags={"test"}
        )
        
        engine = RecommendationEngine()
        recs = engine.content_based_recommendations(user, [item], top_n=1)
        
        assert isinstance(recs, list)

    def test_very_high_scores(self):
        """Handle very high preference/feature scores."""
        user = User(
            user_id="test_001",
            name="Test",
            preferences={"a": 100, "b": 100},
            liked_items=set()
        )
        
        item = Item(
            item_id="test",
            name="Test",
            description="",
            features={"a": 100, "b": 100},
            category="Test",
            tags=set()
        )
        
        engine = RecommendationEngine()
        recs = engine.content_based_recommendations(user, [item], top_n=1)
        
        assert len(recs) == 1

    def test_duplicate_items(self):
        """Handle duplicate items in list."""
        user = DataManager.get_sample_users()[0]
        items = DataManager.get_sample_books()
        
        # Add duplicate
        duplicate_items = items + [items[0]]
        
        engine = RecommendationEngine()
        recs = engine.content_based_recommendations(user, duplicate_items, top_n=5)
        
        assert isinstance(recs, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
