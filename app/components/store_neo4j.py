"""
Neo4j Storage for Knowledge Graph
"""
from typing import Any, Dict, List, Optional

from neo4j import GraphDatabase

from .extractor import Entity, KnowledgeGraph, Relationship


class Neo4jStorage:
    """
    Store and query knowledge graph in Neo4j
    """

    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize Neo4j connection

        Args:
            uri: Neo4j URI (e.g., bolt://localhost:7687)
            user: Neo4j username
            password: Neo4j password
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

        # Test connection
        try:
            self.driver.verify_connectivity()
            print(f"Successfully connected to Neo4j at {uri}")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            print("Neo4j connection closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def clear_database(self):
        """Clear all nodes and relationships from the database"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared")

    def create_entity(
        self,
        name: str,
        entity_type: str,
        properties: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        """
        Create or update an entity node

        Args:
            name: Entity name
            entity_type: Entity type/label
            properties: Additional properties
            embedding: Optional embedding vector
        """
        if properties is None:
            properties = {}

        # Add embedding if provided
        if embedding is not None:
            properties["embedding"] = embedding

        with self.driver.session() as session:
            query = f"""
            MERGE (e:{entity_type} {{name: $name}})
            SET e += $properties
            RETURN e
            """
            session.run(query, name=name, properties=properties)

    def create_relationship(
        self,
        source_name: str,
        target_name: str,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ):
        """
        Create a relationship between entities

        Args:
            source_name: Source entity name
            target_name: Target entity name
            relationship_type: Relationship type
            properties: Additional properties
        """
        if properties is None:
            properties = {}

        # Sanitize relationship type (Neo4j doesn't allow spaces or special chars)
        rel_type = relationship_type.upper().replace(" ", "_").replace("-", "_")

        with self.driver.session() as session:
            query = f"""
            MATCH (s {{name: $source_name}})
            MATCH (t {{name: $target_name}})
            MERGE (s)-[r:{rel_type}]->(t)
            SET r += $properties
            RETURN r
            """
            session.run(
                query, source_name=source_name, target_name=target_name, properties=properties
            )

    def store_knowledge_graph(self, kg: KnowledgeGraph, embeddings: Optional[Dict[str, List[float]]] = None):
        """
        Store a complete knowledge graph

        Args:
            kg: KnowledgeGraph object
            embeddings: Optional dict mapping entity names to embeddings
        """
        if embeddings is None:
            embeddings = {}

        # Create entities
        for entity in kg.entities:
            embedding = embeddings.get(entity.name)
            self.create_entity(
                name=entity.name,
                entity_type=entity.type,
                properties=entity.properties,
                embedding=embedding,
            )

        # Create relationships
        for relationship in kg.relationships:
            self.create_relationship(
                source_name=relationship.source,
                target_name=relationship.target,
                relationship_type=relationship.type,
                properties=relationship.properties,
            )

        print(
            f"Stored {len(kg.entities)} entities and {len(kg.relationships)} relationships"
        )

    def query(self, cypher_query: str, parameters: Optional[Dict] = None) -> List[Dict]:
        """
        Execute a Cypher query

        Args:
            cypher_query: Cypher query string
            parameters: Query parameters

        Returns:
            List of result records as dictionaries
        """
        if parameters is None:
            parameters = {}

        with self.driver.session() as session:
            result = session.run(cypher_query, parameters)
            return [record.data() for record in result]

    def get_entity_by_name(self, name: str) -> Optional[Dict]:
        """
        Get entity by name

        Args:
            name: Entity name

        Returns:
            Entity data or None if not found
        """
        query = "MATCH (n {name: $name}) RETURN n"
        results = self.query(query, {"name": name})
        return results[0] if results else None

    def get_all_entities(self, limit: int = 100) -> List[Dict]:
        """
        Get all entities

        Args:
            limit: Maximum number of entities to return

        Returns:
            List of entity data
        """
        query = "MATCH (n) RETURN n LIMIT $limit"
        return self.query(query, {"limit": limit})

    def get_relationships(
        self, source_name: Optional[str] = None, target_name: Optional[str] = None
    ) -> List[Dict]:
        """
        Get relationships, optionally filtered by source or target

        Args:
            source_name: Optional source entity name
            target_name: Optional target entity name

        Returns:
            List of relationship data
        """
        if source_name and target_name:
            query = """
            MATCH (s {name: $source_name})-[r]->(t {name: $target_name})
            RETURN s.name as source, type(r) as type, t.name as target, properties(r) as properties
            """
            params = {"source_name": source_name, "target_name": target_name}
        elif source_name:
            query = """
            MATCH (s {name: $source_name})-[r]->(t)
            RETURN s.name as source, type(r) as type, t.name as target, properties(r) as properties
            """
            params = {"source_name": source_name}
        elif target_name:
            query = """
            MATCH (s)-[r]->(t {name: $target_name})
            RETURN s.name as source, type(r) as type, t.name as target, properties(r) as properties
            """
            params = {"target_name": target_name}
        else:
            query = """
            MATCH (s)-[r]->(t)
            RETURN s.name as source, type(r) as type, t.name as target, properties(r) as properties
            LIMIT 100
            """
            params = {}

        return self.query(query, params)

    def find_similar_entities(
        self, embedding: List[float], limit: int = 10, threshold: float = 0.7
    ) -> List[Dict]:
        """
        Find entities similar to the given embedding using cosine similarity

        Args:
            embedding: Query embedding vector
            limit: Maximum number of results
            threshold: Minimum similarity threshold

        Returns:
            List of similar entities with similarity scores
        """
        # This requires the Neo4j Vector Search plugin or manual computation
        # For now, we return a placeholder implementation
        query = """
        MATCH (n)
        WHERE n.embedding IS NOT NULL
        RETURN n.name as name, n.embedding as embedding
        LIMIT $limit
        """
        results = self.query(query, {"limit": limit * 2})

        # Compute cosine similarity manually
        import numpy as np

        query_vec = np.array(embedding)
        query_norm = np.linalg.norm(query_vec)

        similar_entities = []
        for result in results:
            entity_embedding = result.get("embedding")
            if entity_embedding:
                entity_vec = np.array(entity_embedding)
                entity_norm = np.linalg.norm(entity_vec)

                if query_norm > 0 and entity_norm > 0:
                    similarity = np.dot(query_vec, entity_vec) / (query_norm * entity_norm)
                    if similarity >= threshold:
                        similar_entities.append(
                            {"name": result["name"], "similarity": float(similarity)}
                        )

        # Sort by similarity and return top results
        similar_entities.sort(key=lambda x: x["similarity"], reverse=True)
        return similar_entities[:limit]
