"""
Main entry point for Knowledge Graph Construction
"""
import argparse
import sys
from pathlib import Path

from app.components.pipeline import KnowledgeGraphPipeline


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Knowledge Graph Construction using LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Input options
    parser.add_argument(
        "--input", "-i", type=str, help="Input file path (PDF or TXT)"
    )
    parser.add_argument(
        "--text", "-t", type=str, help="Input text directly"
    )

    # LLM options
    parser.add_argument(
        "--llm-model",
        type=str,
        default="gpt-4o-mini",
        help="LLM model name (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "--llm-type",
        type=str,
        choices=["openai", "google"],
        default="openai",
        help="LLM type (default: openai)",
    )
    parser.add_argument(
        "--llm-api-key", type=str, help="LLM API key (can also use env vars)"
    )

    # Embedding options
    parser.add_argument(
        "--embedding-model",
        type=str,
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Embedding model name",
    )
    parser.add_argument(
        "--no-embeddings",
        action="store_true",
        help="Don't generate embeddings",
    )

    # Neo4j options
    parser.add_argument(
        "--neo4j-uri",
        type=str,
        help="Neo4j URI (default: from NEO4J_URI env or bolt://localhost:7687)",
    )
    parser.add_argument(
        "--neo4j-user", type=str, help="Neo4j username (default: from NEO4J_USER env or neo4j)"
    )
    parser.add_argument(
        "--neo4j-password",
        type=str,
        help="Neo4j password (default: from NEO4J_PASSWORD env)",
    )

    # Processing options
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Text chunk size (default: 1000)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=200,
        help="Text chunk overlap (default: 200)",
    )
    parser.add_argument(
        "--clear-db",
        action="store_true",
        help="Clear database before storing",
    )

    # Query mode
    parser.add_argument(
        "--query",
        type=str,
        help="Execute a Cypher query and exit",
    )

    args = parser.parse_args()

    # Validate input
    if not args.input and not args.text and not args.query:
        parser.print_help()
        print("\nError: Must provide --input, --text, or --query")
        sys.exit(1)

    try:
        # Initialize pipeline
        print("\n" + "=" * 80)
        print("Knowledge Graph Construction using LLM")
        print("=" * 80)

        pipeline = KnowledgeGraphPipeline(
            neo4j_uri=args.neo4j_uri,
            neo4j_user=args.neo4j_user,
            neo4j_password=args.neo4j_password,
            llm_model=args.llm_model,
            llm_api_key=args.llm_api_key,
            llm_type=args.llm_type,
            embedding_model=args.embedding_model,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        )

        # Query mode
        if args.query:
            print(f"\nExecuting query: {args.query}")
            results = pipeline.query_graph(args.query)
            print(f"\nResults ({len(results)} records):")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result}")
            return

        # Process input
        create_embeddings = not args.no_embeddings

        if args.input:
            input_path = Path(args.input)
            if not input_path.exists():
                print(f"\nError: Input file not found: {args.input}")
                sys.exit(1)

            if input_path.suffix.lower() == ".pdf":
                stats = pipeline.process_pdf(
                    str(input_path),
                    create_embeddings=create_embeddings,
                    clear_db=args.clear_db,
                )
            else:
                # Assume text file
                with open(input_path, "r", encoding="utf-8") as f:
                    text = f.read()
                stats = pipeline.process_text(
                    text, create_embeddings=create_embeddings, clear_db=args.clear_db
                )
        elif args.text:
            stats = pipeline.process_text(
                args.text, create_embeddings=create_embeddings, clear_db=args.clear_db
            )

        # Print statistics
        print("\n" + "=" * 80)
        print("STATISTICS")
        print("=" * 80)
        print(f"Chunks processed: {stats['num_chunks']}")
        print(f"Entities extracted: {stats['num_entities']}")
        print(f"Relationships extracted: {stats['num_relationships']}")
        print(f"Embeddings generated: {'Yes' if stats['has_embeddings'] else 'No'}")
        print("=" * 80)

        # Close pipeline
        pipeline.close()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
