"""
Knowledge Graph Construction Pipeline
Integrates document processing, entity extraction, embedding, and storage
"""
import os
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv

from .chunking import chunk_text, pdf_to_text
from .embedder import Embedder
from .extractor import LLMExtractor, merge_knowledge_graphs
from .store_neo4j import Neo4jStorage

# Load environment variables
load_dotenv()


class KnowledgeGraphPipeline:
    """
    End-to-end pipeline for constructing knowledge graphs from documents
    """

    def __init__(
        self,
        neo4j_uri: Optional[str] = None,
        neo4j_user: Optional[str] = None,
        neo4j_password: Optional[str] = None,
        llm_model: str = "gpt-4o-mini",
        llm_api_key: Optional[str] = None,
        llm_type: str = "openai",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """
        Initialize Knowledge Graph Pipeline

        Args:
            neo4j_uri: Neo4j URI (default: from NEO4J_URI env var)
            neo4j_user: Neo4j username (default: from NEO4J_USER env var)
            neo4j_password: Neo4j password (default: from NEO4J_PASSWORD env var)
            llm_model: LLM model name
            llm_api_key: LLM API key (default: from OPENAI_API_KEY or GOOGLE_API_KEY)
            llm_type: Type of LLM ('openai' or 'google')
            embedding_model: Sentence transformer model name
            chunk_size: Text chunk size
            chunk_overlap: Chunk overlap size
        """
        # Neo4j configuration
        self.neo4j_uri = neo4j_uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = neo4j_user or os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = neo4j_password or os.getenv("NEO4J_PASSWORD", "password123")

        # LLM configuration
        self.llm_type = llm_type
        if llm_api_key is None:
            if llm_type == "openai":
                llm_api_key = os.getenv("OPENAI_API_KEY")
            elif llm_type == "google":
                llm_api_key = os.getenv("GOOGLE_API_KEY")

        # Text processing configuration
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize components
        print("Initializing Knowledge Graph Pipeline...")
        print(f"Neo4j URI: {self.neo4j_uri}")
        print(f"LLM Model: {llm_model} ({llm_type})")
        print(f"Embedding Model: {embedding_model}")

        self.storage = Neo4jStorage(self.neo4j_uri, self.neo4j_user, self.neo4j_password)
        self.extractor = LLMExtractor(
            model_name=llm_model, api_key=llm_api_key, model_type=llm_type
        )
        self.embedder = Embedder(model_name=embedding_model)

        print("Pipeline initialized successfully!")

    def process_text(
        self, text: str, create_embeddings: bool = True, clear_db: bool = False
    ) -> Dict:
        """
        Process text and build knowledge graph

        Args:
            text: Input text
            create_embeddings: Whether to create embeddings for entities
            clear_db: Whether to clear database before storing

        Returns:
            Dictionary with processing statistics
        """
        print("\n" + "=" * 80)
        print("Processing text...")
        print("=" * 80)

        # Clear database if requested
        if clear_db:
            print("Clearing database...")
            self.storage.clear_database()

        # Chunk text
        print(f"\nChunking text (size={self.chunk_size}, overlap={self.chunk_overlap})...")
        chunks = chunk_text(text, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        print(f"Created {len(chunks)} chunks")

        # Extract entities and relationships from each chunk
        print("\nExtracting entities and relationships using LLM...")
        graphs = []
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")
            kg = self.extractor.extract(chunk)
            print(
                f"  - Found {len(kg.entities)} entities and {len(kg.relationships)} relationships"
            )
            graphs.append(kg)

        # Merge all knowledge graphs
        print("\nMerging knowledge graphs...")
        merged_kg = merge_knowledge_graphs(graphs)
        print(
            f"Merged graph: {len(merged_kg.entities)} entities, {len(merged_kg.relationships)} relationships"
        )

        # Create embeddings if requested
        embeddings = {}
        if create_embeddings and merged_kg.entities:
            print("\nGenerating embeddings for entities...")
            entity_names = [e.name for e in merged_kg.entities]
            entity_embeddings = self.embedder.embed_batch(entity_names)
            embeddings = dict(zip(entity_names, entity_embeddings))
            print(f"Generated {len(embeddings)} embeddings")

        # Store in Neo4j
        print("\nStoring knowledge graph in Neo4j...")
        self.storage.store_knowledge_graph(merged_kg, embeddings)

        print("\n" + "=" * 80)
        print("Processing complete!")
        print("=" * 80)

        return {
            "num_chunks": len(chunks),
            "num_entities": len(merged_kg.entities),
            "num_relationships": len(merged_kg.relationships),
            "has_embeddings": create_embeddings,
        }

    def process_pdf(
        self, pdf_path: str, create_embeddings: bool = True, clear_db: bool = False
    ) -> Dict:
        """
        Process PDF document and build knowledge graph

        Args:
            pdf_path: Path to PDF file
            create_embeddings: Whether to create embeddings for entities
            clear_db: Whether to clear database before storing

        Returns:
            Dictionary with processing statistics
        """
        print(f"\nLoading PDF: {pdf_path}")
        text = pdf_to_text(pdf_path)
        print(f"Extracted {len(text)} characters")

        return self.process_text(text, create_embeddings, clear_db)

    def query_graph(self, cypher_query: str, parameters: Optional[Dict] = None) -> List[Dict]:
        """
        Query the knowledge graph

        Args:
            cypher_query: Cypher query string
            parameters: Query parameters

        Returns:
            Query results
        """
        return self.storage.query(cypher_query, parameters)

    def find_similar_entities(
        self, query_text: str, limit: int = 10, threshold: float = 0.7
    ) -> List[Dict]:
        """
        Find entities similar to query text

        Args:
            query_text: Query text
            limit: Maximum number of results
            threshold: Minimum similarity threshold

        Returns:
            List of similar entities
        """
        embedding = self.embedder.embed(query_text)
        return self.storage.find_similar_entities(embedding, limit, threshold)

    def close(self):
        """Close all connections and free resources"""
        self.storage.close()
        self.embedder.clear_cache()
        print("Pipeline closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
