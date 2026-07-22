# Recommendation System

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-Coverage%20Included-brightgreen)
![Code Style](https://img.shields.io/badge/Code%20Style-PEP%208-blue)

A comprehensive, production-quality recommendation system demonstrating multiple algorithms and best practices in machine learning and software engineering.

## 🎯 Overview

This project implements a sophisticated recommendation system with multiple algorithms:

- **Content-Based Filtering**: Matches user preferences with item features using similarity metrics
- **Collaborative Filtering**: Recommends items liked by similar users
- **Hybrid Approach**: Combines content-based and collaborative strategies
- **Category Filtering**: Filtered recommendations by item categories

### Key Features

✅ **Multiple Similarity Metrics**: Cosine, Euclidean, Jaccard  
✅ **Three Recommendation Algorithms**: Content-based, Collaborative, Hybrid  
✅ **Interactive CLI**: User-friendly command-line interface  
✅ **Sample Datasets**: Books, Movies, Online Courses  
✅ **Comprehensive Tests**: 25+ unit tests with edge case coverage  
✅ **Production-Ready Code**: Clean architecture, well-documented, type hints  
✅ **Scalable Design**: Easy to extend with new algorithms or datasets  

## 📋 Architecture

```
recommendation_engine.py      # Core recommendation algorithms
├── SimilarityCalculator       # Similarity metrics (Cosine, Euclidean, Jaccard)
└── RecommendationEngine       # Main engine with 4 recommendation methods

data_manager.py               # Data loading and management
├── DataManager                # Sample data management
└── Dataset methods            # Books, Movies, Courses, Users

cli.py                        # Interactive command-line interface
├── RecommendationCLI          # CLI implementation
└── Interactive/Demo modes     # User interaction

test_recommendation.py        # Comprehensive test suite
├── TestSimilarityCalculator   # Similarity metric tests
├── TestRecommendationEngine   # Algorithm tests
├── TestDataManager            # Data loading tests
└── TestEdgeCases              # Edge case handling
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or extract files):
```bash
git clone https://github.com/yourusername/recommendation-system.git
cd recommendation-system
```

2. **Install dependencies** (optional - pytest for tests):
```bash
pip install pytest
```

3. **Run the interactive demo**:
```bash
python cli.py
```

4. **Run automated demo**:
```bash
python cli.py --demo
```

## 📖 Usage

### Interactive Mode

The CLI provides an interactive interface:

```bash
python cli.py
```

**Features:**
- Select dataset (Books, Movies, Courses, or All)
- Choose existing user or create custom profile
- Select recommendation algorithm
- Adjust number of recommendations
- Beautiful formatted output with match scores

### Running Tests

```bash
# Run all tests
pytest test_recommendation.py -v

# Run specific test class
pytest test_recommendation.py::TestSimilarityCalculator -v

# Run with coverage report
pytest test_recommendation.py --cov=. --cov-report=html
```

### Programmatic Usage

```python
from recommendation_engine import RecommendationEngine, SimilarityMetric
from data_manager import DataManager

# Initialize engine
engine = RecommendationEngine(metric=SimilarityMetric.COSINE)

# Get data
user = DataManager.get_sample_users()[0]
items = DataManager.get_sample_books()

# Get recommendations
recommendations = engine.content_based_recommendations(
    user=user,
    items=items,
    top_n=5,
    exclude_liked=True
)

# Display results
for item, score in recommendations:
    print(f"{item.name}: {score:.2%}")
```

## 🔍 Algorithms

### 1. Content-Based Filtering

**How it works**: Matches user preferences with item features using similarity metrics.

**Best for**: Users with clear preferences, Cold-start problem (new users)

**Similarity Metrics**:
- **Cosine Similarity**: Measures angle between preference and feature vectors
  - Formula: (A·B) / (|A||B|)
  - Range: 0 to 1
  - Best for: High-dimensional sparse data

- **Euclidean Similarity**: Measures distance between vectors
  - Formula: 1 / (1 + distance)
  - Range: 0 to 1
  - Best for: Dense features

- **Jaccard Similarity**: Measures overlap between sets
  - Formula: |A ∩ B| / |A ∪ B|
  - Range: 0 to 1
  - Best for: Tag-based features

### 2. Collaborative Filtering

**How it works**: Finds similar users and recommends items they liked.

**Best for**: Users with implicit feedback, Community insights

**Key Parameter**: k_neighbors (number of similar users to consider)

```python
recommendations = engine.collaborative_filtering_recommendations(
    user=user,
    all_users=users,
    items=items,
    k_neighbors=3  # Consider top 3 similar users
)
```

### 3. Hybrid Approach

**How it works**: Combines content-based and collaborative scores.

**Best for**: Production systems, Balanced recommendations

**Customizable Weights**:
```python
recommendations = engine.hybrid_recommendations(
    user=user,
    all_users=users,
    items=items,
    content_weight=0.6,      # 60% content-based
    collaborative_weight=0.4  # 40% collaborative
)
```

## 📊 Example Outputs

### Content-Based Recommendation Output
```
1. The Pragmatic Programmer
   Category: Technology
   Essential guide to software development best practices
   Match Score: ████████████████░░ 89.50%
   Tags: programming, best-practices, software-engineering, career

2. Clean Code
   Category: Technology
   A handbook of agile software craftsmanship
   Match Score: ████████████████░░ 87.30%
   Tags: programming, code-quality, software-engineering, career
```

## 🧪 Testing

### Test Coverage

- **Similarity Calculator**: 10 tests
- **Recommendation Engine**: 12 tests
- **Data Manager**: 3 tests
- **Edge Cases**: 3 tests
- **Total**: 28 comprehensive tests

### Test Examples

```python
# Test identical vectors have similarity 1.0
def test_cosine_similarity_identical():
    vec1 = {"a": 1, "b": 2}
    vec2 = {"a": 1, "b": 2}
    assert SimilarityCalculator.cosine_similarity(vec1, vec2) == 1.0

# Test Jaccard similarity calculation
def test_jaccard_similarity_partial_overlap():
    set1 = {"a", "b", "c"}
    set2 = {"b", "c", "d"}
    assert SimilarityCalculator.jaccard_similarity(set1, set2) == 0.5

# Test recommendation sorting by score
def test_content_based_sorted_by_score():
    recommendations = engine.content_based_recommendations(user, items, top_n=5)
    scores = [score for _, score in recommendations]
    assert scores == sorted(scores, reverse=True)
```

## 📈 Complexity Analysis

### Time Complexity

| Algorithm | Complexity | Notes |
|-----------|-----------|-------|
| Content-Based | O(n × m) | n=users, m=items; Feature comparison |
| Collaborative | O(n² + n×m) | Find similar users + get recommendations |
| Hybrid | O(n × m + n²) | Combines both approaches |
| Similarity (Cosine) | O(k) | k=number of overlapping features |

### Space Complexity

- **Data Storage**: O(n × m) for user-item preference matrix
- **Recommendation Storage**: O(k) where k=top_n results

## 🛠️ Extending the System

### Adding New Similarity Metric

```python
class SimilarityCalculator:
    @staticmethod
    def manhattan_distance(vec1, vec2):
        """Calculate Manhattan distance."""
        all_keys = set(vec1.keys()) | set(vec2.keys())
        return sum(abs(vec1.get(k, 0) - vec2.get(k, 0)) for k in all_keys)
```

### Adding New Dataset

```python
@staticmethod
def get_sample_podcasts():
    return [
        Item(
            item_id="podcast_001",
            name="Example Podcast",
            description="...",
            features={...},
            category="Podcasts",
            tags={...}
        )
    ]
```

### Adding New Recommendation Algorithm

```python
def knowledge_based_recommendations(
    self,
    user: User,
    items: List[Item],
    knowledge_base: Dict,
    top_n: int = 5
):
    """Implement knowledge-based recommendation."""
    # Your algorithm here
    pass
```

## 📚 Data Structure

### User Object
```python
@dataclass
class User:
    user_id: str                      # Unique identifier
    name: str                         # User name
    preferences: Dict[str, float]     # {feature: score}
    liked_items: Set[str]             # Previously liked item IDs
```

### Item Object
```python
@dataclass
class Item:
    item_id: str                      # Unique identifier
    name: str                         # Item name
    description: str                  # Item description
    features: Dict[str, float]        # {feature: value}
    category: str                     # Item category
    tags: Set[str]                    # Descriptive tags
```

## 🎓 Learning Outcomes

This project demonstrates:

✓ **Recommendation System Concepts**
- Content-based and collaborative filtering
- Hybrid recommendation approaches
- Similarity metrics and calculations

✓ **Software Engineering Best Practices**
- Clean architecture and separation of concerns
- Type hints and comprehensive documentation
- Unit testing and edge case handling

✓ **Algorithm Implementation**
- Vector similarity calculations
- k-nearest neighbors concepts
- Score normalization and weighting

✓ **Data Structures**
- Efficient data organization
- User-item preference matrices
- Feature vector representations

## 🤝 Contributing

Feel free to:
- Add new recommendation algorithms
- Implement additional similarity metrics
- Extend with new datasets
- Improve test coverage
- Optimize performance

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

Created as a portfolio project for software engineering and machine learning demonstration.

## 📮 Support

For questions or issues:
1. Check existing documentation
2. Review test cases for usage examples
3. Examine code comments and docstrings

---

**Key Highlights for Recruiters:**

🎯 **Production Quality**: Clean code with type hints, comprehensive docstrings, error handling  
🧪 **Testing**: 28+ unit tests covering normal and edge cases  
📐 **Algorithms**: Multiple implementation approaches with complexity analysis  
🏗️ **Architecture**: Scalable, modular design easy to extend  
📊 **Documentation**: Professional README with examples and technical depth  
🚀 **Features**: Interactive CLI, multiple datasets, export capabilities  

---

Built with ❤️ | Python 3.8+ | Portfolio Ready
