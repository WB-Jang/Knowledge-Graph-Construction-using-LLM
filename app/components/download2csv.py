"""
Export Neo4j Knowledge Graph data to CSV
"""
import os
from pathlib import Path
from typing import Optional

import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables
load_dotenv()


def export_entities_to_csv(
    uri: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    output_file: str = "entities.csv",
):
    """
    Export all entities from Neo4j to CSV

    Args:
        uri: Neo4j URI (default: from NEO4J_URI env var)
        user: Neo4j username (default: from NEO4J_USER env var)
        password: Neo4j password (default: from NEO4J_PASSWORD env var)
        output_file: Output CSV file path
    """
    # Use environment variables as defaults
    uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = user or os.getenv("NEO4J_USER", "neo4j")
    password = password or os.getenv("NEO4J_PASSWORD", "password123")

    # Connect to Neo4j
    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        with driver.session() as session:
            # Query all entities
            query = "MATCH (n) RETURN n.name AS name, labels(n) AS type, properties(n) AS properties"
            result = session.run(query)
            data = [record.data() for record in result]

            # Create DataFrame
            df = pd.DataFrame(data)

            # Save to CSV
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_file, index=False, encoding="utf-8-sig")

            print(f"Exported {len(df)} entities to {output_file}")

    finally:
        driver.close()


def export_relationships_to_csv(
    uri: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    output_file: str = "relationships.csv",
):
    """
    Export all relationships from Neo4j to CSV

    Args:
        uri: Neo4j URI (default: from NEO4J_URI env var)
        user: Neo4j username (default: from NEO4J_USER env var)
        password: Neo4j password (default: from NEO4J_PASSWORD env var)
        output_file: Output CSV file path
    """
    # Use environment variables as defaults
    uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = user or os.getenv("NEO4J_USER", "neo4j")
    password = password or os.getenv("NEO4J_PASSWORD", "password123")

    # Connect to Neo4j
    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        with driver.session() as session:
            # Query all relationships
            query = """
            MATCH (s)-[r]->(t)
            RETURN s.name AS source, type(r) AS relationship, t.name AS target, properties(r) AS properties
            """
            result = session.run(query)
            data = [record.data() for record in result]

            # Create DataFrame
            df = pd.DataFrame(data)

            # Save to CSV
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_file, index=False, encoding="utf-8-sig")

            print(f"Exported {len(df)} relationships to {output_file}")

    finally:
        driver.close()


def main():
    """Main function for exporting data"""
    print("Exporting Knowledge Graph to CSV...")

    # Export entities
    export_entities_to_csv(output_file="outputs/entities.csv")

    # Export relationships
    export_relationships_to_csv(output_file="outputs/relationships.csv")

    print("\nExport complete!")


if __name__ == "__main__":
    main()

