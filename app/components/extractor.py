"""
LLM-based Entity and Relationship Extractor for Knowledge Graph Construction
"""
import json
import re
from typing import Any, Dict, List, Optional, Tuple

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class Entity(BaseModel):
    """Entity model for knowledge graph"""

    name: str = Field(description="Name of the entity")
    type: str = Field(description="Type/category of the entity")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties")


class Relationship(BaseModel):
    """Relationship model for knowledge graph"""

    source: str = Field(description="Source entity name")
    target: str = Field(description="Target entity name")
    type: str = Field(description="Relationship type")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties")


class KnowledgeGraph(BaseModel):
    """Knowledge Graph model"""

    entities: List[Entity] = Field(default_factory=list)
    relationships: List[Relationship] = Field(default_factory=list)


class LLMExtractor:
    """
    Extract entities and relationships from text using LLM
    Optimized for RTX-4080 with 8GB VRAM
    """

    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.0,
        api_key: Optional[str] = None,
        model_type: str = "openai",
    ):
        """
        Initialize LLM Extractor

        Args:
            model_name: Name of the model to use
            temperature: Temperature for generation
            api_key: API key for the model
            model_type: Type of model ('openai' or 'google')
        """
        self.model_name = model_name
        self.temperature = temperature
        self.model_type = model_type

        if model_type == "openai":
            self.llm = ChatOpenAI(
                model=model_name, temperature=temperature, api_key=api_key, max_tokens=4096
            )
        elif model_type == "google":
            self.llm = ChatGoogleGenerativeAI(
                model=model_name, temperature=temperature, google_api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        self.extraction_prompt = self._create_extraction_prompt()

    def _create_extraction_prompt(self) -> ChatPromptTemplate:
        """Create prompt template for entity and relationship extraction"""
        template = """You are an expert at extracting entities and relationships from text to build a knowledge graph.

Given the following text, extract:
1. Entities: Important concepts, objects, people, organizations, or any significant nouns
2. Relationships: Connections between entities

Text:
{text}

Output the result as a valid JSON object with this structure:
{{
  "entities": [
    {{
      "name": "entity name",
      "type": "entity type (e.g., Person, Organization, Concept, Location, etc.)",
      "properties": {{}}
    }}
  ],
  "relationships": [
    {{
      "source": "source entity name",
      "target": "target entity name", 
      "type": "relationship type (e.g., works_for, located_in, related_to, etc.)",
      "properties": {{}}
    }}
  ]
}}

Important:
- Extract only entities that are explicitly mentioned or strongly implied
- Entity names should be concise and standardized
- Relationship types should be clear and descriptive
- Ensure source and target entity names match exactly with entity names in the entities list
- Return ONLY the JSON object, no additional text

JSON Output:"""
        return ChatPromptTemplate.from_template(template)

    def extract(self, text: str) -> KnowledgeGraph:
        """
        Extract entities and relationships from text

        Args:
            text: Input text to extract from

        Returns:
            KnowledgeGraph object containing extracted entities and relationships
        """
        try:
            # Generate extraction using LLM
            chain = self.extraction_prompt | self.llm
            response = chain.invoke({"text": text})

            # Parse response
            content = response.content.strip()

            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", content, re.DOTALL)
            if json_match:
                content = json_match.group(1)

            # Parse JSON
            data = json.loads(content)

            # Create KnowledgeGraph
            entities = [Entity(**e) for e in data.get("entities", [])]
            relationships = [Relationship(**r) for r in data.get("relationships", [])]

            return KnowledgeGraph(entities=entities, relationships=relationships)

        except Exception as e:
            print(f"Error during extraction: {e}")
            print(f"Response content: {content if 'content' in locals() else 'N/A'}")
            return KnowledgeGraph(entities=[], relationships=[])

    def extract_batch(self, texts: List[str]) -> List[KnowledgeGraph]:
        """
        Extract entities and relationships from multiple texts

        Args:
            texts: List of input texts

        Returns:
            List of KnowledgeGraph objects
        """
        return [self.extract(text) for text in texts]


def merge_knowledge_graphs(graphs: List[KnowledgeGraph]) -> KnowledgeGraph:
    """
    Merge multiple knowledge graphs into one

    Args:
        graphs: List of KnowledgeGraph objects

    Returns:
        Merged KnowledgeGraph
    """
    all_entities = []
    all_relationships = []
    entity_map = {}  # Map to deduplicate entities by name

    for graph in graphs:
        for entity in graph.entities:
            if entity.name not in entity_map:
                entity_map[entity.name] = entity
                all_entities.append(entity)
            else:
                # Merge properties if entity already exists
                existing = entity_map[entity.name]
                existing.properties.update(entity.properties)

        all_relationships.extend(graph.relationships)

    # Deduplicate relationships
    unique_relationships = []
    seen = set()
    for rel in all_relationships:
        key = (rel.source, rel.target, rel.type)
        if key not in seen:
            seen.add(key)
            unique_relationships.append(rel)

    return KnowledgeGraph(entities=all_entities, relationships=unique_relationships)
