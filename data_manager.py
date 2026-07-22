"""
Data Manager Module

Handles sample datasets and data loading for the recommendation system.
Includes sample data for books, movies, and tech courses.
"""

from recommendation_engine import User, Item
from typing import List, Dict
import json


class DataManager:
    """Manages datasets and provides sample data."""

    @staticmethod
    def get_sample_books() -> List[Item]:
        """Get sample book dataset."""
        return [
            Item(
                item_id="book_001",
                name="The Pragmatic Programmer",
                description="Essential guide to software development best practices",
                features={
                    "technical": 0.9,
                    "educational": 0.85,
                    "inspiring": 0.7,
                    "practical": 0.95,
                    "depth": 0.8
                },
                category="Technology",
                tags={"programming", "best-practices", "software-engineering", "career"}
            ),
            Item(
                item_id="book_002",
                name="Clean Code",
                description="A handbook of agile software craftsmanship",
                features={
                    "technical": 0.85,
                    "educational": 0.9,
                    "inspiring": 0.75,
                    "practical": 0.9,
                    "depth": 0.85
                },
                category="Technology",
                tags={"programming", "code-quality", "software-engineering", "career"}
            ),
            Item(
                item_id="book_003",
                name="Atomic Habits",
                description="Transform your habits and build lasting success",
                features={
                    "motivational": 0.95,
                    "practical": 0.9,
                    "psychological": 0.8,
                    "depth": 0.7,
                    "entertaining": 0.75
                },
                category="Self-Help",
                tags={"habits", "productivity", "personal-development", "psychology"}
            ),
            Item(
                item_id="book_004",
                name="Thinking, Fast and Slow",
                description="Insights into the two systems of human thinking",
                features={
                    "psychological": 0.95,
                    "educational": 0.9,
                    "depth": 0.95,
                    "inspiring": 0.7,
                    "technical": 0.4
                },
                category="Psychology",
                tags={"psychology", "decision-making", "behavioral-science", "education"}
            ),
            Item(
                item_id="book_005",
                name="Introduction to Algorithms",
                description="Comprehensive textbook on algorithms and data structures",
                features={
                    "technical": 0.95,
                    "educational": 0.95,
                    "depth": 0.98,
                    "practical": 0.85,
                    "entertaining": 0.3
                },
                category="Technology",
                tags={"algorithms", "data-structures", "computer-science", "education"}
            ),
            Item(
                item_id="book_006",
                name="Sapiens",
                description="A brief history of humankind",
                features={
                    "educational": 0.9,
                    "depth": 0.85,
                    "entertaining": 0.85,
                    "inspiring": 0.75,
                    "psychological": 0.7
                },
                category="History",
                tags={"history", "anthropology", "society", "education"}
            ),
        ]

    @staticmethod
    def get_sample_movies() -> List[Item]:
        """Get sample movie dataset."""
        return [
            Item(
                item_id="movie_001",
                name="The Social Network",
                description="The story of Facebook's founding",
                features={
                    "entertaining": 0.9,
                    "educational": 0.7,
                    "inspiring": 0.8,
                    "technical": 0.6,
                    "drama": 0.85
                },
                category="Drama",
                tags={"startup", "technology", "drama", "biography"}
            ),
            Item(
                item_id="movie_002",
                name="Inception",
                description="Mind-bending sci-fi thriller",
                features={
                    "entertaining": 0.95,
                    "thought-provoking": 0.9,
                    "technical": 0.7,
                    "inspiring": 0.65,
                    "action": 0.85
                },
                category="Sci-Fi",
                tags={"sci-fi", "thriller", "mind-bending", "action"}
            ),
            Item(
                item_id="movie_003",
                name="The Shawshank Redemption",
                description="Classic tale of hope and friendship",
                features={
                    "emotional": 0.95,
                    "entertaining": 0.9,
                    "inspiring": 0.95,
                    "depth": 0.9,
                    "drama": 0.95
                },
                category="Drama",
                tags={"drama", "emotional", "classic", "inspiration"}
            ),
            Item(
                item_id="movie_004",
                name="The Matrix",
                description="Reality-bending action sci-fi",
                features={
                    "entertaining": 0.95,
                    "thought-provoking": 0.85,
                    "action": 0.95,
                    "technical": 0.75,
                    "inspiring": 0.7
                },
                category="Sci-Fi",
                tags={"sci-fi", "action", "philosophy", "classic"}
            ),
            Item(
                item_id="movie_005",
                name="Parasite",
                description="Award-winning Korean thriller",
                features={
                    "entertaining": 0.9,
                    "thought-provoking": 0.9,
                    "drama": 0.85,
                    "depth": 0.9,
                    "artistic": 0.9
                },
                category="Thriller",
                tags={"thriller", "drama", "social-commentary", "award-winning"}
            ),
        ]

    @staticmethod
    def get_sample_courses() -> List[Item]:
        """Get sample online course dataset."""
        return [
            Item(
                item_id="course_001",
                name="Machine Learning Specialization",
                description="Comprehensive ML course from basics to advanced",
                features={
                    "technical": 0.95,
                    "educational": 0.95,
                    "practical": 0.9,
                    "depth": 0.9,
                    "difficulty": 0.8
                },
                category="Technology",
                tags={"machine-learning", "python", "ai", "data-science"}
            ),
            Item(
                item_id="course_002",
                name="Web Development Bootcamp",
                description="Full-stack web development from scratch",
                features={
                    "technical": 0.9,
                    "practical": 0.95,
                    "educational": 0.85,
                    "difficulty": 0.7,
                    "community": 0.8
                },
                category="Technology",
                tags={"web-development", "javascript", "full-stack", "beginner-friendly"}
            ),
            Item(
                item_id="course_003",
                name="Data Science Fundamentals",
                description="Essential data science concepts and tools",
                features={
                    "technical": 0.85,
                    "educational": 0.9,
                    "practical": 0.85,
                    "depth": 0.75,
                    "difficulty": 0.6
                },
                category="Technology",
                tags={"data-science", "python", "statistics", "visualization"}
            ),
            Item(
                item_id="course_004",
                name="Personal Productivity Mastery",
                description="Build effective habits and maximize productivity",
                features={
                    "practical": 0.9,
                    "motivational": 0.85,
                    "educational": 0.7,
                    "psychological": 0.8,
                    "difficulty": 0.3
                },
                category="Self-Help",
                tags={"productivity", "habits", "personal-development", "time-management"}
            ),
            Item(
                item_id="course_005",
                name="System Design Interview Prep",
                description="Master system design for technical interviews",
                features={
                    "technical": 0.95,
                    "practical": 0.85,
                    "educational": 0.9,
                    "depth": 0.9,
                    "difficulty": 0.85
                },
                category="Technology",
                tags={"system-design", "interviews", "architecture", "advanced"}
            ),
        ]

    @staticmethod
    def get_sample_users() -> List[User]:
        """Get sample user dataset."""
        return [
            User(
                user_id="user_001",
                name="Alice",
                preferences={
                    "technical": 0.9,
                    "educational": 0.85,
                    "practical": 0.8,
                    "depth": 0.75,
                    "entertaining": 0.5
                },
                liked_items={"book_001", "course_001"}
            ),
            User(
                user_id="user_002",
                name="Bob",
                preferences={
                    "entertaining": 0.9,
                    "action": 0.85,
                    "thought-provoking": 0.7,
                    "technical": 0.4,
                    "depth": 0.6
                },
                liked_items={"movie_002", "movie_004"}
            ),
            User(
                user_id="user_003",
                name="Charlie",
                preferences={
                    "practical": 0.85,
                    "educational": 0.8,
                    "motivational": 0.8,
                    "technical": 0.7,
                    "depth": 0.75
                },
                liked_items={"book_003", "course_003"}
            ),
            User(
                user_id="user_004",
                name="Diana",
                preferences={
                    "emotional": 0.85,
                    "inspiring": 0.9,
                    "depth": 0.85,
                    "entertaining": 0.8,
                    "technical": 0.3
                },
                liked_items={"movie_003", "book_004"}
            ),
        ]

    @staticmethod
    def get_all_items() -> List[Item]:
        """Get all sample items from all categories."""
        return (
            DataManager.get_sample_books() +
            DataManager.get_sample_movies() +
            DataManager.get_sample_courses()
        )

    @staticmethod
    def export_user_data(user: User, filename: str = "user_profile.json") -> None:
        """Export user profile to JSON file."""
        user_data = {
            "user_id": user.user_id,
            "name": user.name,
            "preferences": user.preferences,
            "liked_items": list(user.liked_items)
        }
        with open(filename, 'w') as f:
            json.dump(user_data, f, indent=2)
        print(f"User profile exported to {filename}")

    @staticmethod
    def import_user_data(filename: str) -> User:
        """Import user profile from JSON file."""
        with open(filename, 'r') as f:
            user_data = json.load(f)
        return User(
            user_id=user_data["user_id"],
            name=user_data["name"],
            preferences=user_data["preferences"],
            liked_items=set(user_data["liked_items"])
        )
