# Usage Guide

## Basic Usage

### 1. Process Text

```bash
poetry run python app/main.py --text "Your text here" --clear-db
```

### 2. Process Text File

```bash
poetry run python app/main.py --input data/sample.txt --clear-db
```

### 3. Process PDF

```bash
poetry run python app/main.py --input data/document.pdf --clear-db
```

### 4. Query Knowledge Graph

```bash
# Get all nodes
poetry run python app/main.py --query "MATCH (n) RETURN n LIMIT 10"

# Get all relationships
poetry run python app/main.py --query "MATCH (s)-[r]->(t) RETURN s, r, t LIMIT 10"
```

## Advanced Options

### LLM Configuration

```bash
# Use OpenAI (default)
poetry run python app/main.py --input data/sample.txt \
  --llm-type openai \
  --llm-model gpt-4o-mini

# Use Google Gemini
poetry run python app/main.py --input data/sample.txt \
  --llm-type google \
  --llm-model gemini-1.5-flash
```

### Chunking Options

```bash
poetry run python app/main.py --input data/large_document.txt \
  --chunk-size 2000 \
  --chunk-overlap 400
```

### Disable Embeddings

```bash
poetry run python app/main.py --input data/sample.txt \
  --no-embeddings
```

### Custom Neo4j Connection

```bash
poetry run python app/main.py --input data/sample.txt \
  --neo4j-uri bolt://custom-host:7687 \
  --neo4j-user admin \
  --neo4j-password secret
```

## Python API

### Basic Usage

```python
from app.components.pipeline import KnowledgeGraphPipeline

# Initialize pipeline
with KnowledgeGraphPipeline() as pipeline:
    # Process text
    stats = pipeline.process_text(
        text="Your text here",
        create_embeddings=True,
        clear_db=False
    )
    
    # Query graph
    results = pipeline.query_graph("MATCH (n) RETURN n LIMIT 10")
```

### Process PDF

```python
from app.components.pipeline import KnowledgeGraphPipeline

with KnowledgeGraphPipeline() as pipeline:
    stats = pipeline.process_pdf(
        pdf_path="data/document.pdf",
        create_embeddings=True,
        clear_db=True
    )
    print(f"Extracted {stats['num_entities']} entities")
```

### Custom Configuration

```python
from app.components.pipeline import KnowledgeGraphPipeline

pipeline = KnowledgeGraphPipeline(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password123",
    llm_model="gpt-4o-mini",
    llm_type="openai",
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    chunk_size=1000,
    chunk_overlap=200
)

try:
    pipeline.process_text("Your text")
finally:
    pipeline.close()
```

### Find Similar Entities

```python
from app.components.pipeline import KnowledgeGraphPipeline

with KnowledgeGraphPipeline() as pipeline:
    # Find entities similar to query
    similar = pipeline.find_similar_entities(
        query_text="artificial intelligence",
        limit=10,
        threshold=0.7
    )
    
    for entity in similar:
        print(f"{entity['name']}: {entity['similarity']:.3f}")
```

## Neo4j Queries

### Basic Queries

```cypher
-- Get all nodes
MATCH (n) RETURN n LIMIT 25

-- Get all relationships
MATCH (s)-[r]->(t) RETURN s, r, t LIMIT 25

-- Count nodes by type
MATCH (n) RETURN labels(n) as type, count(n) as count

-- Count relationships by type
MATCH ()-[r]->() RETURN type(r) as relationship, count(r) as count
```

### Advanced Queries

```cypher
-- Find specific entity and its connections
MATCH (n {name: "OpenAI"})-[r]-(m)
RETURN n, r, m

-- Find path between two entities
MATCH path = (a {name: "AI"})-[*..3]-(b {name: "Neural Networks"})
RETURN path

-- Find highly connected nodes (hubs)
MATCH (n)-[r]-()
WITH n, count(r) as connections
WHERE connections > 5
RETURN n.name, connections
ORDER BY connections DESC
```

## Export Data

### Export to CSV

```python
from app.components.download2csv import export_entities_to_csv, export_relationships_to_csv

# Export entities
export_entities_to_csv(output_file="outputs/entities.csv")

# Export relationships
export_relationships_to_csv(output_file="outputs/relationships.csv")
```

### Export from Command Line

```bash
poetry run python -m app.components.download2csv
```

## Tips and Best Practices

### 1. Chunk Size Selection
- **Small chunks (500-1000)**: Better for extracting fine-grained relationships
- **Large chunks (2000-4000)**: Better for capturing broader context
- Default 1000 is a good balance

### 2. Model Selection
- **gpt-4o-mini**: Fast and cost-effective (recommended)
- **gpt-4o**: More accurate but slower and more expensive
- **gemini-1.5-flash**: Fast Google alternative
- **gemini-1.5-pro**: More capable Google model

### 3. Memory Management (RTX-4080 8GB)
- Use smaller embedding models for larger datasets
- Process in batches if dealing with very large documents
- Clear embeddings cache periodically

### 4. Embedding Models
- **all-MiniLM-L6-v2**: Fast, 384 dimensions (default)
- **all-mpnet-base-v2**: More accurate, 768 dimensions
- **paraphrase-multilingual-MiniLM-L12-v2**: For multilingual text

### 5. Graph Quality
- Clear and concise text produces better results
- Pre-process documents to remove noise
- Review and refine extracted entities manually if needed

## Examples

See `app/example.py` for a complete working example.

### Process Multiple Documents

```python
from pathlib import Path
from app.components.pipeline import KnowledgeGraphPipeline

docs_dir = Path("data/documents")
pdf_files = docs_dir.glob("*.pdf")

with KnowledgeGraphPipeline() as pipeline:
    for i, pdf_file in enumerate(pdf_files):
        print(f"Processing {pdf_file.name}...")
        stats = pipeline.process_pdf(
            str(pdf_file),
            create_embeddings=True,
            clear_db=(i == 0)  # Clear DB only for first file
        )
        print(f"  Entities: {stats['num_entities']}")
        print(f"  Relationships: {stats['num_relationships']}")
```

### Batch Processing with Progress

```python
from tqdm import tqdm
from app.components.pipeline import KnowledgeGraphPipeline

texts = [...]  # Your list of texts

with KnowledgeGraphPipeline() as pipeline:
    for i, text in enumerate(tqdm(texts)):
        pipeline.process_text(
            text,
            create_embeddings=True,
            clear_db=(i == 0)
        )
```
