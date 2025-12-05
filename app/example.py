"""
Example usage of Knowledge Graph Construction Pipeline
"""
import os
from dotenv import load_dotenv
from app.components.pipeline import KnowledgeGraphPipeline

# Load environment variables
load_dotenv()

# Example text about AI and Machine Learning
EXAMPLE_TEXT = """
Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines. 
Machine Learning is a subset of AI that focuses on the development of algorithms that can learn from data.

Deep Learning is a subset of Machine Learning that uses neural networks with multiple layers. 
Neural networks are computing systems inspired by the biological neural networks in animal brains.

OpenAI is an AI research organization founded by Elon Musk and Sam Altman in 2015.
OpenAI developed GPT-4, a large language model that can generate human-like text.

Google DeepMind created AlphaGo, an AI program that defeated the world champion in the game of Go.
DeepMind was acquired by Google in 2014.

PyTorch is a machine learning framework developed by Facebook AI Research.
TensorFlow is another popular machine learning framework created by Google Brain.
"""


def main():
    """Main example function"""
    print("=" * 80)
    print("Knowledge Graph Construction Example")
    print("=" * 80)

    # Initialize pipeline
    # Make sure to set environment variables:
    # - NEO4J_URI (default: bolt://localhost:7687)
    # - NEO4J_USER (default: neo4j)
    # - NEO4J_PASSWORD (required)
    # - OPENAI_API_KEY or GOOGLE_API_KEY (required for LLM)
    
    try:
        with KnowledgeGraphPipeline(
            llm_model="gpt-4o-mini",  # or "gemini-1.5-flash" for Google
            llm_type="openai",  # or "google" for Google Gemini
            chunk_size=500,  # Smaller chunks for this example
            chunk_overlap=50,
        ) as pipeline:
            
            # Process the example text
            print("\n1. Processing example text...")
            stats = pipeline.process_text(
                EXAMPLE_TEXT,
                create_embeddings=True,
                clear_db=True,  # Clear database for clean example
            )
            
            print("\n2. Querying the knowledge graph...")
            
            # Query 1: Get all entities
            print("\n   a) All entities:")
            entities = pipeline.query_graph("MATCH (n) RETURN n.name as name, labels(n) as type LIMIT 20")
            for entity in entities:
                print(f"      - {entity['name']} ({', '.join(entity['type'])})")
            
            # Query 2: Get all relationships
            print("\n   b) All relationships:")
            relationships = pipeline.query_graph(
                "MATCH (s)-[r]->(t) RETURN s.name as source, type(r) as relationship, t.name as target LIMIT 20"
            )
            for rel in relationships:
                print(f"      - {rel['source']} --[{rel['relationship']}]--> {rel['target']}")
            
            # Query 3: Find entities connected to "OpenAI"
            print("\n   c) Entities connected to OpenAI:")
            openai_connections = pipeline.query_graph(
                "MATCH (s {name: 'OpenAI'})-[r]-(t) RETURN s.name as entity, type(r) as relationship, t.name as connected",
                {"name": "OpenAI"}
            )
            for conn in openai_connections:
                print(f"      - {conn['entity']} --[{conn['relationship']}]-- {conn['connected']}")
            
            # Query 4: Find similar entities
            print("\n   d) Entities similar to 'artificial intelligence':")
            similar = pipeline.find_similar_entities("artificial intelligence", limit=5, threshold=0.5)
            for entity in similar:
                print(f"      - {entity['name']} (similarity: {entity['similarity']:.3f})")
            
            print("\n" + "=" * 80)
            print("Example completed successfully!")
            print("=" * 80)
            print("\nYou can view the knowledge graph in Neo4j Browser:")
            print(f"  URL: http://localhost:7474")
            print(f"  Username: {os.getenv('NEO4J_USER', 'neo4j')}")
            print(f"  Password: {os.getenv('NEO4J_PASSWORD', '***')}")
            print("\nTry running this query in Neo4j Browser:")
            print("  MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 25")
            print("=" * 80)
            
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        print("\n\nMake sure:")
        print("1. Neo4j is running (docker-compose up neo4j)")
        print("2. Environment variables are set (.env file or export)")
        print("3. You have an OpenAI or Google API key")


if __name__ == "__main__":
    main()
