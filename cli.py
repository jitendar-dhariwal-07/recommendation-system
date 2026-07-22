"""
Command-Line Interface for Recommendation System

Provides interactive CLI for users to get recommendations based on their preferences.
"""

from recommendation_engine import (
    RecommendationEngine, SimilarityMetric, User, Item
)
from data_manager import DataManager
from typing import List, Dict, Set
import sys


class RecommendationCLI:
    """Interactive CLI for the recommendation system."""

    def __init__(self):
        """Initialize the CLI."""
        self.engine = RecommendationEngine(metric=SimilarityMetric.COSINE)
        self.all_items = DataManager.get_all_items()
        self.all_users = DataManager.get_sample_users()
        self.current_user = None
        self.categories = self._extract_categories()

    def _extract_categories(self) -> Set[str]:
        """Extract all unique categories from items."""
        return {item.category for item in self.all_items}

    def print_welcome(self) -> None:
        """Print welcome message."""
        print("\n" + "="*60)
        print("   RECOMMENDATION SYSTEM - Interactive Demo")
        print("="*60)
        print("\nWelcome! This system recommends items based on your preferences.")
        print("Choose from: Books, Movies, Online Courses\n")

    def get_dataset_choice(self) -> List[Item]:
        """Let user choose dataset."""
        print("Which type of items would you like recommendations for?")
        print("1. Books")
        print("2. Movies")
        print("3. Online Courses")
        print("4. All Categories")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            return DataManager.get_sample_books()
        elif choice == "2":
            return DataManager.get_sample_movies()
        elif choice == "3":
            return DataManager.get_sample_courses()
        elif choice == "4":
            return self.all_items
        else:
            print("Invalid choice. Showing all items.")
            return self.all_items

    def create_user_profile(self) -> User:
        """Create or select a user profile."""
        print("\n" + "-"*60)
        print("PROFILE SETUP")
        print("-"*60)

        print("\nChoose an option:")
        print("1. Use existing sample user")
        print("2. Create new user profile")

        choice = input("\nEnter choice (1-2): ").strip()

        if choice == "1":
            return self.select_existing_user()
        elif choice == "2":
            return self.create_new_user()
        else:
            print("Invalid choice. Using first sample user.")
            return self.all_users[0]

    def select_existing_user(self) -> User:
        """Select from existing sample users."""
        print("\nAvailable users:")
        for i, user in enumerate(self.all_users, 1):
            print(f"{i}. {user.name}")

        choice = input("\nSelect user (1-4): ").strip()
        try:
            idx = int(choice) - 1
            return self.all_users[idx]
        except (ValueError, IndexError):
            print("Invalid choice. Using Alice.")
            return self.all_users[0]

    def create_new_user(self) -> User:
        """Create a new user with custom preferences."""
        user_id = f"user_{len(self.all_users) + 1:03d}"
        name = input("\nEnter your name: ").strip() or "Anonymous"

        print("\nRate your preferences (0.0 - 1.0, where 1.0 is highest):")
        preferences: Dict[str, float] = {}

        preference_keys = [
            "technical", "educational", "practical", "entertaining",
            "inspiring", "depth", "action", "drama", "thought-provoking",
            "motivational", "emotional", "psychological"
        ]

        for key in preference_keys:
            try:
                value = float(input(f"  {key}: ").strip() or "0.5")
                value = max(0.0, min(1.0, value))  # Clamp to 0-1
                preferences[key] = value
            except ValueError:
                preferences[key] = 0.5

        return User(
            user_id=user_id,
            name=name,
            preferences=preferences,
            liked_items=set()
        )

    def display_user_profile(self, user: User) -> None:
        """Display user profile information."""
        print("\n" + "-"*60)
        print(f"USER PROFILE: {user.name} ({user.user_id})")
        print("-"*60)
        print("\nPreferences:")
        for key, value in sorted(user.preferences.items()):
            bar = "█" * int(value * 20) + "░" * (20 - int(value * 20))
            print(f"  {key:20s} {bar} {value:.2f}")

        if user.liked_items:
            print(f"\nLiked Items: {', '.join(user.liked_items)}")
        else:
            print("\nNo liked items yet.")

    def get_recommendation_method(self) -> str:
        """Let user choose recommendation algorithm."""
        print("\n" + "-"*60)
        print("RECOMMENDATION METHOD")
        print("-"*60)

        print("\nChoose recommendation algorithm:")
        print("1. Content-Based (matches your preferences with item features)")
        print("2. Collaborative (recommends what similar users liked)")
        print("3. Hybrid (combines content-based and collaborative)")
        print("4. Category Filtered (recommendations from selected categories)")

        choice = input("\nEnter choice (1-4): ").strip()
        return choice

    def get_recommendations(
        self,
        user: User,
        items: List[Item],
        method: str,
        top_n: int = 5
    ) -> List[tuple]:
        """Get recommendations based on selected method."""
        if method == "1":
            return self.engine.content_based_recommendations(user, items, top_n)
        elif method == "2":
            return self.engine.collaborative_filtering_recommendations(
                user, self.all_users, items, top_n
            )
        elif method == "3":
            return self.engine.hybrid_recommendations(
                user, self.all_users, items, top_n
            )
        elif method == "4":
            return self.get_category_filtered_recommendations(user, items, top_n)
        else:
            print("Invalid method. Using content-based recommendations.")
            return self.engine.content_based_recommendations(user, items, top_n)

    def get_category_filtered_recommendations(
        self,
        user: User,
        items: List[Item],
        top_n: int = 5
    ) -> List[tuple]:
        """Get recommendations filtered by categories."""
        print("\nAvailable categories:")
        categories = sorted(self.categories)
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")

        choice = input("\nEnter category number (or comma-separated for multiple): ").strip()

        selected_categories = []
        for num in choice.split(","):
            try:
                idx = int(num.strip()) - 1
                selected_categories.append(categories[idx])
            except (ValueError, IndexError):
                pass

        if not selected_categories:
            selected_categories = categories

        return self.engine.category_filtered_recommendations(
            user, items, selected_categories, top_n
        )

    def display_recommendations(
        self,
        recommendations: List[tuple],
        method_name: str
    ) -> None:
        """Display recommendations beautifully."""
        print("\n" + "="*60)
        print(f"RECOMMENDATIONS ({method_name})")
        print("="*60)

        if not recommendations:
            print("\nNo recommendations found. Try different preferences!")
            return

        for i, (item, score) in enumerate(recommendations, 1):
            bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
            print(f"\n{i}. {item.name}")
            print(f"   Category: {item.category}")
            print(f"   {item.description}")
            print(f"   Match Score: {bar} {score:.2%}")
            print(f"   Tags: {', '.join(sorted(item.tags))}")

    def get_top_n(self) -> int:
        """Get number of recommendations to display."""
        try:
            n = int(input("\nHow many recommendations? (default 5): ").strip() or "5")
            return max(1, min(10, n))  # Clamp to 1-10
        except ValueError:
            return 5

    def run_interactive_session(self) -> None:
        """Run an interactive recommendation session."""
        self.print_welcome()

        # Step 1: Get dataset
        items = self.get_dataset_choice()
        print(f"\nLoaded {len(items)} items from selected category/categories.")

        # Step 2: Create/select user
        self.current_user = self.create_user_profile()
        self.display_user_profile(self.current_user)

        # Step 3: Get recommendations
        while True:
            method = self.get_recommendation_method()
            top_n = self.get_top_n()

            recommendations = self.get_recommendations(self.current_user, items, method, top_n)

            method_names = {
                "1": "Content-Based Filtering",
                "2": "Collaborative Filtering",
                "3": "Hybrid Approach",
                "4": "Category Filtered"
            }
            self.display_recommendations(recommendations, method_names.get(method, "Unknown"))

            # Ask if user wants more recommendations
            choice = input("\n\nTry another method? (yes/no): ").strip().lower()
            if choice not in ["yes", "y"]:
                break

        self.print_goodbye()

    def print_goodbye(self) -> None:
        """Print goodbye message."""
        print("\n" + "="*60)
        print("   Thank you for using the Recommendation System!")
        print("="*60 + "\n")

    def run_demo(self) -> None:
        """Run automated demo showing all features."""
        print("\n" + "="*60)
        print("   AUTOMATED DEMO - Recommendation System Features")
        print("="*60)

        # Demo 1: Content-based recommendations
        print("\n" + "-"*60)
        print("DEMO 1: Content-Based Filtering")
        print("-"*60)
        user = self.all_users[0]
        items = DataManager.get_sample_books()
        print(f"User: {user.name}")
        print(f"Top preferences: {dict(sorted(user.preferences.items(), key=lambda x: x[1], reverse=True)[:3])}")
        
        recs = self.engine.content_based_recommendations(user, items, top_n=3)
        self.display_recommendations(recs, "Content-Based")

        # Demo 2: Collaborative filtering
        print("\n" + "-"*60)
        print("DEMO 2: Collaborative Filtering")
        print("-"*60)
        user = self.all_users[1]
        items = DataManager.get_sample_movies()
        print(f"User: {user.name}")
        
        recs = self.engine.collaborative_filtering_recommendations(
            user, self.all_users, items, top_n=3
        )
        self.display_recommendations(recs, "Collaborative")

        # Demo 3: Hybrid recommendations
        print("\n" + "-"*60)
        print("DEMO 3: Hybrid Recommendations")
        print("-"*60)
        user = self.all_users[2]
        items = DataManager.get_sample_courses()
        print(f"User: {user.name}")
        
        recs = self.engine.hybrid_recommendations(user, self.all_users, items, top_n=3)
        self.display_recommendations(recs, "Hybrid")

        self.print_goodbye()


def main():
    """Main entry point."""
    cli = RecommendationCLI()

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        cli.run_demo()
    else:
        try:
            cli.run_interactive_session()
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            cli.print_goodbye()
        except Exception as e:
            print(f"\nError: {e}")
            cli.print_goodbye()


if __name__ == "__main__":
    main()
