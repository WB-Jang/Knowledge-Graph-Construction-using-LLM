"""Test configuration and fixtures"""
import pytest


@pytest.fixture
def sample_text():
    """Sample text for testing"""
    return """
    Artificial Intelligence (AI) is a branch of computer science.
    Machine Learning is a subset of AI that focuses on learning from data.
    Deep Learning uses neural networks with multiple layers.
    """


@pytest.fixture
def sample_entities():
    """Sample entities for testing"""
    from app.components.extractor import Entity
    
    return [
        Entity(name="Artificial Intelligence", type="Concept"),
        Entity(name="Machine Learning", type="Concept"),
        Entity(name="Deep Learning", type="Concept"),
    ]


@pytest.fixture
def sample_relationships():
    """Sample relationships for testing"""
    from app.components.extractor import Relationship
    
    return [
        Relationship(
            source="Artificial Intelligence",
            target="Machine Learning",
            type="includes"
        ),
        Relationship(
            source="Machine Learning",
            target="Deep Learning",
            type="includes"
        ),
    ]
