"""
Recommendation System Engine

This module implements multiple recommendation algorithms:
- Content-based filtering using similarity metrics
- Collaborative filtering concepts
- Hybrid recommendations
"""

from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import math


class SimilarityMetric(Enum):
    """Available similarity metrics for recommendation."""
    EUCLIDEAN = "euclidean"
    COSINE = "cosine"
    JACCARD = "jaccard"


@dataclass
class User:
    """Represents a user with preferences."""
    user_id: str
    name: str
    preferences: Dict[str, float]  # {feature: score}
    liked_items: Set[str]  # Item IDs user has liked


@dataclass
class Item:
    """Represents an item to recommend."""
    item_id: str
    name: str
    description: str
    features: Dict[str, float]  # {feature: value}
    category: str
    tags: Set[str]


class SimilarityCalculator:
    """Calculates similarity between vectors using various metrics."""

    @staticmethod
    def euclidean_distance(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Calculate Euclidean distance between two vectors.
        Lower distance = higher similarity.
        """
        all_keys = set(vec1.keys()) | set(vec2.keys())
        sum_squares = sum(
            (vec1.get(key, 0) - vec2.get(key, 0)) ** 2
            for key in all_keys
        )
        return math.sqrt(sum_squares)

    @staticmethod
    def euclidean_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Convert Euclidean distance to similarity score (0-1).
        Used for recommendation matching.
        """
        distance = SimilarityCalculator.euclidean_distance(vec1, vec2)
        # Normalize to 0-1 scale: similarity = 1 / (1 + distance)
        return 1 / (1 + distance)

    @staticmethod
    def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Calculate Cosine similarity (angle between vectors).
        Range: -1 to 1 (typically 0-1 for preferences).
        Best for: High-dimensional sparse data.
        """
        all_keys = set(vec1.keys()) & set(vec2.keys())
        
        if not all_keys:
            return 0.0
        
        dot_product = sum(vec1[key] * vec2[key] for key in all_keys)
        magnitude1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        magnitude2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)

    @staticmethod
    def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
        """
        Calculate Jaccard similarity for sets (e.g., tags, interests).
        Range: 0 to 1.
        Formula: |intersection| / |union|
        """
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0


class RecommendationEngine:
    """Main recommendation engine with multiple algorithms."""

    def __init__(self, metric: SimilarityMetric = SimilarityMetric.COSINE):
        """
        Initialize the recommendation engine.
        
        Args:
            metric: Similarity metric to use for calculations
        """
        self.metric = metric
        self.similarity_calc = SimilarityCalculator()

    def content_based_recommendations(
        self,
        user: User,
        items: List[Item],
        top_n: int = 5,
        exclude_liked: bool = True
    ) -> List[Tuple[Item, float]]:
        """
        Generate content-based recommendations.
        
        Matches user preferences with item features.
        
        Args:
            user: User object with preferences
            items: List of available items
            top_n: Number of recommendations to return
            exclude_liked: Whether to exclude already-liked items
            
        Returns:
            List of (Item, similarity_score) tuples, sorted by score
        """
        recommendations = []
        
        for item in items:
            # Skip already liked items if requested
            if exclude_liked and item.item_id in user.liked_items:
                continue
            
            # Calculate similarity based on selected metric
            if self.metric == SimilarityMetric.COSINE:
                score = self.similarity_calc.cosine_similarity(
                    user.preferences, item.features
                )
            elif self.metric == SimilarityMetric.EUCLIDEAN:
                score = self.similarity_calc.euclidean_similarity(
                    user.preferences, item.features
                )
            else:  # JACCARD - use tags
                score = self.similarity_calc.jaccard_similarity(
                    set(user.preferences.keys()),
                    item.tags
                )
            
            if score > 0:
                recommendations.append((item, score))
        
        # Sort by score (descending) and return top N
        return sorted(recommendations, key=lambda x: x[1], reverse=True)[:top_n]

    def collaborative_filtering_recommendations(
        self,
        user: User,
        all_users: List[User],
        items: List[Item],
        top_n: int = 5,
        k_neighbors: int = 3
    ) -> List[Tuple[Item, float]]:
        """
        Generate recommendations using collaborative filtering concepts.
        
        Find similar users and recommend items they liked.
        
        Args:
            user: Target user
            all_users: All users in the system
            items: Available items
            top_n: Number of recommendations to return
            k_neighbors: Number of similar users to consider
            
        Returns:
            List of (Item, recommendation_score) tuples
        """
        # Find similar users
        similar_users = []
        for other_user in all_users:
            if other_user.user_id == user.user_id:
                continue
            
            similarity = self.similarity_calc.cosine_similarity(
                user.preferences, other_user.preferences
            )
            similar_users.append((other_user, similarity))
        
        # Get k most similar users
        similar_users.sort(key=lambda x: x[1], reverse=True)
        k_nearest = similar_users[:k_neighbors]
        
        # Collect items liked by similar users
        item_scores: Dict[str, float] = {}
        for similar_user, user_similarity in k_nearest:
            for liked_item_id in similar_user.liked_items:
                # Skip if user already liked it
                if liked_item_id in user.liked_items:
                    continue
                
                # Score is product of user similarity and item relevance
                if liked_item_id not in item_scores:
                    item_scores[liked_item_id] = 0
                item_scores[liked_item_id] += user_similarity

        # Convert to recommendations
        recommendations = []
        item_map = {item.item_id: item for item in items}
        
        for item_id, score in item_scores.items():
            if item_id in item_map:
                recommendations.append((item_map[item_id], score))
        
        return sorted(recommendations, key=lambda x: x[1], reverse=True)[:top_n]

    def hybrid_recommendations(
        self,
        user: User,
        all_users: List[User],
        items: List[Item],
        top_n: int = 5,
        content_weight: float = 0.6,
        collaborative_weight: float = 0.4
    ) -> List[Tuple[Item, float]]:
        """
        Generate hybrid recommendations combining content-based and collaborative.
        
        Args:
            user: Target user
            all_users: All users in the system
            items: Available items
            top_n: Number of recommendations to return
            content_weight: Weight for content-based scores (0-1)
            collaborative_weight: Weight for collaborative scores (0-1)
            
        Returns:
            List of (Item, hybrid_score) tuples
        """
        # Get both types of recommendations
        content_recs = self.content_based_recommendations(
            user, items, top_n=len(items), exclude_liked=True
        )
        collaborative_recs = self.collaborative_filtering_recommendations(
            user, all_users, items, top_n=len(items)
        )
        
        # Create score maps
        content_scores = {item.item_id: score for item, score in content_recs}
        collab_scores = {item.item_id: score for item, score in collaborative_recs}
        
        # Combine scores
        hybrid_scores: Dict[str, float] = {}
        all_item_ids = set(content_scores.keys()) | set(collab_scores.keys())
        
        for item_id in all_item_ids:
            content_score = content_scores.get(item_id, 0)
            collab_score = collab_scores.get(item_id, 0)
            
            # Normalize scores to 0-1 if needed
            hybrid_scores[item_id] = (
                content_weight * content_score +
                collaborative_weight * collab_score
            )
        
        # Convert to recommendations
        item_map = {item.item_id: item for item in items}
        recommendations = [
            (item_map[item_id], score)
            for item_id, score in hybrid_scores.items()
            if item_id in item_map
        ]
        
        return sorted(recommendations, key=lambda x: x[1], reverse=True)[:top_n]

    def category_filtered_recommendations(
        self,
        user: User,
        items: List[Item],
        categories: List[str],
        top_n: int = 5
    ) -> List[Tuple[Item, float]]:
        """
        Generate recommendations filtered by specific categories.
        
        Args:
            user: Target user
            items: Available items
            categories: Categories to filter by
            top_n: Number of recommendations per category
            
        Returns:
            List of (Item, similarity_score) tuples
        """
        filtered_items = [item for item in items if item.category in categories]
        return self.content_based_recommendations(user, filtered_items, top_n)
