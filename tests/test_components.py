"""
Basic tests for Knowledge Graph Construction components
"""
import pytest

from app.components.chunking import chunk_text
from app.components.extractor import Entity, KnowledgeGraph, Relationship


def test_chunk_text():
    """Test text chunking"""
    text = "This is a test. " * 100
    chunks = chunk_text(text, chunk_size=50, chunk_overlap=10)
    
    assert len(chunks) > 0
    assert all(len(chunk) <= 60 for chunk in chunks)  # Allow some overflow


def test_entity_creation():
    """Test Entity model"""
    entity = Entity(name="Test Entity", type="Concept", properties={"key": "value"})
    
    assert entity.name == "Test Entity"
    assert entity.type == "Concept"
    assert entity.properties["key"] == "value"


def test_relationship_creation():
    """Test Relationship model"""
    rel = Relationship(
        source="Entity A",
        target="Entity B",
        type="relates_to",
        properties={"strength": "high"}
    )
    
    assert rel.source == "Entity A"
    assert rel.target == "Entity B"
    assert rel.type == "relates_to"
    assert rel.properties["strength"] == "high"


def test_knowledge_graph_creation():
    """Test KnowledgeGraph model"""
    entity1 = Entity(name="AI", type="Concept")
    entity2 = Entity(name="Machine Learning", type="Concept")
    rel = Relationship(source="AI", target="Machine Learning", type="includes")
    
    kg = KnowledgeGraph(entities=[entity1, entity2], relationships=[rel])
    
    assert len(kg.entities) == 2
    assert len(kg.relationships) == 1
    assert kg.entities[0].name == "AI"
    assert kg.relationships[0].type == "includes"


def test_empty_knowledge_graph():
    """Test empty KnowledgeGraph"""
    kg = KnowledgeGraph()
    
    assert len(kg.entities) == 0
    assert len(kg.relationships) == 0
