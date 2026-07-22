# Contributing to Recommendation System

Thank you for your interest in contributing to this project! This guide explains how to extend and improve the recommendation system.

## 📋 Table of Contents

1. [Adding New Similarity Metrics](#adding-new-similarity-metrics)
2. [Adding New Recommendation Algorithms](#adding-new-recommendation-algorithms)
3. [Extending Datasets](#extending-datasets)
4. [Code Style and Standards](#code-style-and-standards)
5. [Testing New Features](#testing-new-features)
6. [Documentation](#documentation)

## Adding New Similarity Metrics

### 1. Implement the Metric

Add your similarity metric to `SimilarityCalculator` class in `recommendation_engine.py`:

```python
@staticmethod
def manhattan_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """
    Calculate Manhattan (L1) similarity.
    
    Also known as taxicab distance. Good for sparse, high-dimensional data.
    
    Args:
        vec1: First preference/feature vector
        vec2: Second preference/feature vector
        
    Returns:
        Similarity score between 0 and 1
    """
    all_keys = set(vec1.keys()) | set(vec2.keys())
    sum_abs_diff = sum(
        abs(vec1.get(key, 0) - vec2.get(key, 0))
        for key in all_keys
    )
    # Normalize: similarity = 1 / (1 + distance)
    return 1 / (1 + sum_abs_diff)
```

### 2. Add to SimilarityMetric Enum

```python
class SimilarityMetric(Enum):
    """Available similarity metrics for recommendation."""
    EUCLIDEAN = "euclidean"
    COSINE = "cosine"
    JACCARD = "jaccard"
    MANHATTAN = "manhattan"  # New metric
```

### 3. Update RecommendationEngine

Add the metric to the `content_based_recommendations` method:

```python
def content_based_recommendations(self, ...):
    if self.metric == SimilarityMetric.COSINE:
        score = self.similarity_calc.cosine_similarity(...)
    elif self.metric == SimilarityMetric.EUCLIDEAN:
        score = self.similarity_calc.euclidean_similarity(...)
    elif self.metric == SimilarityMetric.MANHATTAN:  # New
        score = self.similarity_calc.manhattan_similarity(...)
    # ...
```

### 4. Add Tests

Create comprehensive tests in `test_recommendation.py`:

```python
def test_manhattan_similarity_identical():
    """Manhattan similarity of identical vectors should be 1.0"""
    vec1 = {"a": 1, "b": 2}
    vec2 = {"a": 1, "b": 2}
    
    similarity = SimilarityCalculator.manhattan_similarity(vec1, vec2)
    assert similarity == pytest.approx(1.0)

def test_manhattan_similarity_range():
    """Manhattan similarity should be in range [0, 1]"""
    vec1 = {"a": 0, "b": 0}
    vec2 = {"a": 10, "b": 10}
    
    similarity = SimilarityCalculator.manhattan_similarity(vec1, vec2)
    assert 0 <= similarity <= 1
```

## Adding New Recommendation Algorithms

### 1. Understand the Pattern

All recommendation methods:
- Take a `User` and list of `Item`s as input
- Return `List[Tuple[Item, float]]` (item and score)
- Sort by score descending
- Respect `top_n` parameter

### 2. Implement the Algorithm

```python
def knowledge_based_recommendations(
    self,
    user: User,
    items: List[Item],
    knowledge_base: Dict[str, List[str]],
    top_n: int = 5
) -> List[Tuple[Item, float]]:
    """
    Generate knowledge-based recommendations using domain expertise.
    
    This approach uses explicit knowledge rules and domain expertise
    to recommend items that match user requirements.
    
    Args:
        user: Target user for recommendations
        items: Available items to recommend from
        knowledge_base: Domain knowledge rules (e.g., {skill: recommended_items})
        top_n: Maximum number of recommendations to return
        
    Returns:
        List of (Item, score) tuples sorted by score descending
        
    Time Complexity: O(n * k) where n=items, k=avg rules per item
    Space Complexity: O(n) for results storage
    """
    item_scores: Dict[str, float] = {}
    
    # Extract user interests from preferences
    user_interests = {
        key for key, score in user.preferences.items()
        if score > 0.5
    }
    
    # Apply knowledge base rules
    for interest in user_interests:
        if interest in knowledge_base:
            recommended_ids = knowledge_base[interest]
            for item_id in recommended_ids:
                if item_id not in user.liked_items:
                    item_scores[item_id] = item_scores.get(item_id, 0) + 1
    
    # Convert to Item objects with scores
    item_map = {item.item_id: item for item in items}
    recommendations = [
        (item_map[item_id], score)
        for item_id, score in item_scores.items()
        if item_id in item_map
    ]
    
    # Sort and return top N
    return sorted(recommendations, key=lambda x: x[1], reverse=True)[:top_n]
```

### 3. Add Documentation

Include in method docstring:
- **Purpose**: What does this algorithm do?
- **Best For**: When should this algorithm be used?
- **Assumptions**: What assumptions does it make?
- **Parameters**: Detailed parameter explanations
- **Complexity**: Time and space complexity
- **Example**: Usage example

### 4. Add Comprehensive Tests

```python
def test_knowledge_based_returns_items(self, engine):
    """Knowledge-based recommendations should return Item objects."""
    user = self.get_sample_user()
    items = self.get_sample_items()
    knowledge_base = {"interest1": ["item_001", "item_002"]}
    
    recs = engine.knowledge_based_recommendations(
        user, items, knowledge_base, top_n=5
    )
    
    assert isinstance(recs, list)
    assert all(isinstance(item, Item) for item, _ in recs)

def test_knowledge_based_respects_top_n(self, engine):
    """Should return at most top_n recommendations."""
    for n in [1, 3, 5]:
        recs = engine.knowledge_based_recommendations(..., top_n=n)
        assert len(recs) <= n

def test_knowledge_based_excludes_liked(self, engine):
    """Should not recommend already-liked items."""
    user = self.get_sample_user_with_likes()
    recs = engine.knowledge_based_recommendations(...)
    
    rec_ids = {item.item_id for item, _ in recs}
    assert not rec_ids.intersection(user.liked_items)
```

## Extending Datasets

### 1. Add New Dataset Method

```python
@staticmethod
def get_sample_podcasts() -> List[Item]:
    """Get sample podcast dataset for recommendations."""
    return [
        Item(
            item_id="podcast_001",
            name="Example Podcast",
            description="A fascinating discussion about technology",
            features={
                "technical": 0.85,
                "educational": 0.90,
                "entertaining": 0.75,
                "depth": 0.80,
                "inspiring": 0.65
            },
            category="Podcasts",
            tags={"technology", "education", "interviews", "discussions"}
        ),
        # Add more podcasts...
    ]
```

### 2. Update get_all_items()

```python
@staticmethod
def get_all_items() -> List[Item]:
    """Get all sample items from all categories."""
    return (
        DataManager.get_sample_books() +
        DataManager.get_sample_movies() +
        DataManager.get_sample_courses() +
        DataManager.get_sample_podcasts()  # Add new dataset
    )
```

### 3. Update CLI

Add dataset option to `RecommendationCLI`:

```python
def get_dataset_choice(self) -> List[Item]:
    print("Which type of items would you like recommendations for?")
    print("1. Books")
    print("2. Movies")
    print("3. Online Courses")
    print("4. Podcasts")  # New option
    print("5. All Categories")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "4":
        return DataManager.get_sample_podcasts()
    # ...
```

### 4. Add Tests

```python
def test_podcasts_dataset_loaded():
    """Podcast dataset should load correctly."""
    podcasts = DataManager.get_sample_podcasts()
    assert len(podcasts) > 0
    
def test_podcasts_have_required_fields():
    """Each podcast should have required fields."""
    podcasts = DataManager.get_sample_podcasts()
    for podcast in podcasts:
        assert podcast.item_id
        assert podcast.name
        assert podcast.features
        assert podcast.category == "Podcasts"
```

## Code Style and Standards

### 1. Type Hints

Always use type hints:

```python
# Good
def recommend(user: User, items: List[Item], top_n: int) -> List[Tuple[Item, float]]:
    pass

# Avoid
def recommend(user, items, top_n):
    pass
```

### 2. Docstrings

Use comprehensive docstrings following NumPy style:

```python
def method(param1: str, param2: int) -> float:
    """
    Brief description of what the method does.
    
    Longer description explaining the purpose, algorithm, or approach
    if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2, with constraints if any
        
    Returns:
        Description of return value and its type/range
        
    Raises:
        ValueError: When input validation fails
        
    Example:
        >>> result = method("test", 42)
        >>> print(result)
        0.75
        
    Note:
        Any important notes about performance or usage
        
    See Also:
        related_method: Related functionality
    """
    pass
```

### 3. Naming Conventions

```python
# Constants
MAX_RECOMMENDATIONS = 10
DEFAULT_K_NEIGHBORS = 3

# Functions/methods (snake_case)
def get_recommendations():
    pass

# Classes (PascalCase)
class RecommendationEngine:
    pass

# Private methods (leading underscore)
def _calculate_score():
    pass
```

### 4. Code Organization

```python
# Group related functionality
class RecommendationEngine:
    # 1. Initialization
    def __init__(self):
        pass
    
    # 2. Public methods
    def public_method(self):
        pass
    
    # 3. Private helper methods
    def _helper_method(self):
        pass
```

## Testing New Features

### 1. Test Structure

```python
class TestNewFeature:
    """Tests for new feature."""
    
    @pytest.fixture
    def setup(self):
        """Setup test data."""
        return create_test_data()
    
    def test_normal_case(self, setup):
        """Test normal/happy path."""
        pass
    
    def test_edge_case(self, setup):
        """Test edge cases."""
        pass
    
    def test_error_handling(self, setup):
        """Test error conditions."""
        pass
```

### 2. Test Coverage

Aim for high coverage:

```bash
# Run tests with coverage
pytest test_recommendation.py --cov=. --cov-report=html

# View report
open htmlcov/index.html
```

### 3. Test Data

Use fixtures for reusable test data:

```python
@pytest.fixture
def sample_user():
    return User(
        user_id="test_001",
        name="Test User",
        preferences={"technical": 0.8, "educational": 0.7},
        liked_items={"item_001"}
    )
```

## Documentation

### 1. Update README

Add section for new feature:

```markdown
### New Feature Name

**Description**: What does it do?

**Usage**:
```python
# Code example
```

**Best For**: When to use this feature
```

### 2. Add Examples

Add example to `examples.py`:

```python
def example_N_new_feature():
    """
    Example N: Description
    
    Demonstrates the new feature.
    """
    print("\n" + "="*60)
    print("EXAMPLE N: New Feature")
    print("="*60)
    
    # Example code
```

### 3. Docstring Completeness

Ensure all public methods have:
- Purpose description
- Parameter documentation
- Return value documentation
- Complexity analysis
- Usage examples

## Pull Request Checklist

Before submitting a PR:

- [ ] Code follows style guidelines
- [ ] All type hints are present
- [ ] Docstrings are comprehensive
- [ ] Tests are added and passing
- [ ] Code coverage is maintained or improved
- [ ] README is updated if needed
- [ ] Examples are provided if applicable
- [ ] No breaking changes to existing API
- [ ] Commit messages are clear

## Questions?

Feel free to:
1. Review existing code for patterns
2. Check test cases for usage examples
3. Look at similar implementations

---

Thank you for contributing! Your improvements help make this project better.
