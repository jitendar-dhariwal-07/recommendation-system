"""
Example Usage of the Recommendation System

This file demonstrates various ways to use the recommendation system.
Run individual examples with: python -c "from examples import *; example_1()"
"""

from recommendation_engine import (
    RecommendationEngine, SimilarityMetric, User, Item, SimilarityCalculator
)
from data_manager import DataManager


def example_1_basic_content_based():
    """
    Example 1: Basic Content-Based Recommendation
    
    Get book recommendations based on user preferences.
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Content-Based Recommendation")
    print("="*60)
    
    # Initialize engine
    engine = RecommendationEngine(metric=SimilarityMetric.COSINE)
    
    # Get first sample user and all books
    user = DataManager.get_sample_users()[0]
    books = DataManager.get_sample_books()
    
    print(f"\nUser: {user.name}")
    print(f"Top preferences: {dict(sorted(user.preferences.items(), key=lambda x: x[1], reverse=True)[:3])}")
    
    # Get recommendations
    recommendations = engine.content_based_recommendations(user, books, top_n=3)
    
    print("\nTop 3 Recommended Books:")
    for i, (item, score) in enumerate(recommendations, 1):
        print(f"{i}. {item.name}")
        print(f"   Match: {score:.2%}")
        print(f"   Description: {item.description}\n")


def example_2_similarity_metrics():
    """
    Example 2: Compare Different Similarity Metrics
    
    See how different metrics affect recommendations.
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Comparing Similarity Metrics")
    print("="*60)
    
    user = DataManager.get_sample_users()[1]
    movies = DataManager.get_sample_movies()
    
    print(f"\nUser: {user.name}")
    
    for metric in [SimilarityMetric.COSINE, SimilarityMetric.EUCLIDEAN]:
        engine = RecommendationEngine(metric=metric)
        recs = engine.content_based_recommendations(user, movies, top_n=2)
        
        print(f"\n{metric.value.upper()} Similarity Metric:")
        for item, score in recs:
            print(f"  - {item.name}: {score:.2%}")


def example_3_collaborative_filtering():
    """
    Example 3: Collaborative Filtering Recommendations
    
    Recommend items liked by similar users.
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Collaborative Filtering")
    print("="*60)
    
    engine = RecommendationEngine()
    
    target_user = DataManager.get_sample_users()[0]
    all_users = DataManager.get_sample_users()
    courses = DataManager.get_sample_courses()
    
    print(f"\nFinding users similar to {target_user.name}...")
    
    # Get collaborative recommendations
    recs = engine.collaborative_filtering_recommendations(
        user=target_user,
        all_users=all_users,
        items=courses,
        top_n=3,
        k_neighbors=2
    )
    
    print(f"\nRecommended Courses (based on similar users' preferences):")
    for i, (item, score) in enumerate(recs, 1):
        print(f"{i}. {item.name}")
        print(f"   Score: {score:.2%}")
        print(f"   {item.description}\n")


def example_4_hybrid_recommendations():
    """
    Example 4: Hybrid Recommendations
    
    Combine content-based and collaborative approaches.
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Hybrid Recommendations")
    print("="*60)
    
    engine = RecommendationEngine()
    
    user = DataManager.get_sample_users()[2]
    all_users = DataManager.get_sample_users()
    items = DataManager.get_all_items()
    
    print(f"\nUser: {user.name}")
    print("Combining 60% content-based + 40% collaborative\n")
    
    recs = engine.hybrid_recommendations(
        user=user,
        all_users=all_users,
        items=items,
        top_n=3,
        content_weight=0.6,
        collaborative_weight=0.4
    )
    
    for i, (item, score) in enumerate(recs, 1):
        print(f"{i}. {item.name} ({item.category})")
        print(f"   Hybrid Score: {score:.2%}")
        print()


def example_5_category_filtering():
    """
    Example 5: Category-Based Filtering
    
    Get recommendations filtered by specific categories.
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Category-Based Recommendations")
    print("="*60)
    
    engine = RecommendationEngine()
    
    user = DataManager.get_sample_users()[1]
    all_items = DataManager.get_all_items()
    
    print(f"\nUser: {user.name}")
    print("Categories: Technology\n")
    
    recs = engine.category_filtered_recommendations(
        user=user,
        items=all_items,
        categories=["Technology"],
        top_n=3
    )
    
    for i, (item, score) in enumerate(recs, 1):
        print(f"{i}. {item.name}")
        print(f"   Category: {item.category}")
        print(f"   Match: {score:.2%}\n")


def example_6_similarity_calculations():
    """
    Example 6: Direct Similarity Calculations
    
    See how similarity metrics work in detail.
    """
    print("\n" + "="*60)
    print("EXAMPLE 6: Direct Similarity Calculations")
    print("="*60)
    
    # User preferences
    user_prefs = {
        "technical": 0.9,
        "educational": 0.8,
        "practical": 0.7
    }
    
    # Two different items
    item1_features = {
        "technical": 0.95,
        "educational": 0.85,
        "practical": 0.6
    }
    
    item2_features = {
        "technical": 0.3,
        "educational": 0.9,
        "practical": 0.95
    }
    
    calc = SimilarityCalculator()
    
    print(f"\nUser Preferences: {user_prefs}")
    print(f"\nItem 1 Features: {item1_features}")
    print(f"Item 2 Features: {item2_features}\n")
    
    # Cosine similarity
    cos_sim_1 = calc.cosine_similarity(user_prefs, item1_features)
    cos_sim_2 = calc.cosine_similarity(user_prefs, item2_features)
    
    print("COSINE SIMILARITY (vector angle):")
    print(f"  Item 1: {cos_sim_1:.4f} ({cos_sim_1:.2%})")
    print(f"  Item 2: {cos_sim_2:.4f} ({cos_sim_2:.2%})")
    print(f"  Winner: Item {'1' if cos_sim_1 > cos_sim_2 else '2'}\n")
    
    # Euclidean similarity
    euc_sim_1 = calc.euclidean_similarity(user_prefs, item1_features)
    euc_sim_2 = calc.euclidean_similarity(user_prefs, item2_features)
    
    print("EUCLIDEAN SIMILARITY (distance-based):")
    print(f"  Item 1: {euc_sim_1:.4f} ({euc_sim_1:.2%})")
    print(f"  Item 2: {euc_sim_2:.4f} ({euc_sim_2:.2%})")
    print(f"  Winner: Item {'1' if euc_sim_1 > euc_sim_2 else '2'}\n")


def example_7_custom_user_profile():
    """
    Example 7: Creating Custom User Profile
    
    Create and get recommendations for a custom user.
    """
    print("\n" + "="*60)
    print("EXAMPLE 7: Custom User Profile")
    print("="*60)
    
    # Create custom user
    custom_user = User(
        user_id="user_custom_001",
        name="Tech Enthusiast",
        preferences={
            "technical": 0.95,
            "educational": 0.90,
            "practical": 0.85,
            "depth": 0.80,
            "entertaining": 0.40
        },
        liked_items=set()
    )
    
    print(f"\nCreated Custom User: {custom_user.name}")
    print("Preferences:")
    for key, value in sorted(custom_user.preferences.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(value * 15) + "░" * (15 - int(value * 15))
        print(f"  {key:15s} {bar} {value:.2f}")
    
    # Get recommendations
    engine = RecommendationEngine()
    items = DataManager.get_sample_books()
    
    recs = engine.content_based_recommendations(custom_user, items, top_n=3)
    
    print("\nTop Recommendations:")
    for i, (item, score) in enumerate(recs, 1):
        print(f"{i}. {item.name} ({score:.2%})")


def example_8_exclude_liked_items():
    """
    Example 8: Excluding Already-Liked Items
    
    Demonstrate recommendation filtering.
    """
    print("\n" + "="*60)
    print("EXAMPLE 8: Excluding Already-Liked Items")
    print("="*60)
    
    user = DataManager.get_sample_users()[0]
    books = DataManager.get_sample_books()
    
    print(f"\nUser: {user.name}")
    print(f"Already liked: {user.liked_items}\n")
    
    engine = RecommendationEngine()
    
    # With exclusion
    recs_filtered = engine.content_based_recommendations(
        user=user,
        items=books,
        top_n=5,
        exclude_liked=True
    )
    
    # Without exclusion
    recs_all = engine.content_based_recommendations(
        user=user,
        items=books,
        top_n=5,
        exclude_liked=False
    )
    
    print(f"With exclusion (top_n=5): {len(recs_filtered)} items")
    print(f"Without exclusion (top_n=5): {len(recs_all)} items")
    
    print("\nRecommendations (with exclusion):")
    for item, score in recs_filtered:
        print(f"  - {item.name}: {score:.2%}")


def example_9_dataset_exploration():
    """
    Example 9: Exploring Available Datasets
    
    Overview of available data.
    """
    print("\n" + "="*60)
    print("EXAMPLE 9: Dataset Exploration")
    print("="*60)
    
    books = DataManager.get_sample_books()
    movies = DataManager.get_sample_movies()
    courses = DataManager.get_sample_courses()
    users = DataManager.get_sample_users()
    
    print(f"\nAvailable Items:")
    print(f"  Books:   {len(books)}")
    print(f"  Movies:  {len(movies)}")
    print(f"  Courses: {len(courses)}")
    print(f"  Total:   {len(books) + len(movies) + len(courses)}")
    
    print(f"\nAvailable Users: {len(users)}")
    for user in users:
        print(f"  - {user.name}: {len(user.liked_items)} liked items")
    
    print("\nSample Book:")
    book = books[0]
    print(f"  ID: {book.item_id}")
    print(f"  Name: {book.name}")
    print(f"  Category: {book.category}")
    print(f"  Features: {dict(sorted(book.features.items(), key=lambda x: x[1], reverse=True)[:3])}")
    print(f"  Tags: {', '.join(book.tags)}")


def example_10_performance_comparison():
    """
    Example 10: Performance Comparison
    
    Compare recommendation algorithms.
    """
    print("\n" + "="*60)
    print("EXAMPLE 10: Algorithm Performance Comparison")
    print("="*60)
    
    import time
    
    engine = RecommendationEngine()
    user = DataManager.get_sample_users()[0]
    all_users = DataManager.get_sample_users()
    items = DataManager.get_all_items()
    
    algorithms = [
        ("Content-Based", lambda: engine.content_based_recommendations(user, items, top_n=5)),
        ("Collaborative", lambda: engine.collaborative_filtering_recommendations(user, all_users, items, top_n=5)),
        ("Hybrid", lambda: engine.hybrid_recommendations(user, all_users, items, top_n=5)),
    ]
    
    print(f"\nRunning with {len(items)} items, {len(all_users)} users\n")
    
    for name, func in algorithms:
        start = time.time()
        for _ in range(100):  # Run 100 times
            func()
        elapsed = time.time() - start
        per_call = elapsed / 100 * 1000  # Convert to milliseconds
        
        print(f"{name:20s}: {per_call:.4f} ms per call")


# Run all examples
if __name__ == "__main__":
    example_1_basic_content_based()
    example_2_similarity_metrics()
    example_3_collaborative_filtering()
    example_4_hybrid_recommendations()
    example_5_category_filtering()
    example_6_similarity_calculations()
    example_7_custom_user_profile()
    example_8_exclude_liked_items()
    example_9_dataset_exploration()
    example_10_performance_comparison()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60 + "\n")
