# Project Summary: Knowledge Graph Construction using LLM

## Overview

This project implements a comprehensive system for constructing Knowledge Graphs from text documents using Large Language Models (LLMs). The system is optimized for RTX-4080 GPU (8GB VRAM) and includes complete Docker containerization, DevContainer support, and Poetry dependency management.

## Key Features

### 1. LLM-Based Knowledge Extraction
- **Entity Extraction**: Automatically identifies entities (people, organizations, concepts, etc.)
- **Relationship Extraction**: Detects relationships between entities
- **Multiple LLM Support**: OpenAI GPT and Google Gemini models
- **Structured Output**: JSON-formatted extraction results

### 2. Graph Storage and Querying
- **Neo4j Integration**: Professional graph database for storing knowledge graphs
- **Cypher Queries**: Powerful graph query language support
- **Vector Search**: Similarity-based entity search using embeddings
- **Data Export**: CSV export functionality for entities and relationships

### 3. Document Processing
- **Text Chunking**: Intelligent text splitting with overlap
- **PDF Support**: Direct PDF document processing
- **Batch Processing**: Handle multiple documents efficiently
- **Korean Law Documents**: Special support for Korean legal documents

### 4. Embedding Generation
- **Sentence Transformers**: State-of-the-art text embeddings
- **GPU Acceleration**: Optimized for RTX-4080
- **Batch Processing**: Efficient embedding generation
- **Similarity Search**: Find related entities using embeddings

### 5. Development Environment
- **Docker Compose**: Complete containerized setup
- **DevContainer**: VSCode development container support
- **Poetry**: Modern Python dependency management
- **GPU Support**: NVIDIA Docker Runtime integration

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Input Documents                         │
│              (PDF, TXT, or Direct Text)                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│               Text Chunking (chunking.py)                   │
│         - Split text into manageable chunks                 │
│         - Configurable size and overlap                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│          Entity & Relationship Extraction                   │
│                 (extractor.py)                              │
│         - LLM-based extraction (GPT/Gemini)                 │
│         - Structured JSON output                            │
│         - Entity and relationship models                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│            Embedding Generation                             │
│               (embedder.py)                                 │
│         - Sentence Transformers                             │
│         - GPU acceleration                                  │
│         - Batch processing                                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Neo4j Storage                                  │
│            (store_neo4j.py)                                 │
│         - Graph database storage                            │
│         - Cypher query support                              │
│         - Vector similarity search                          │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Core Technologies
- **Python 3.10+**: Programming language
- **PyTorch 2.3.0**: Deep learning framework
- **CUDA 12.1**: GPU acceleration
- **Neo4j 5.15**: Graph database

### LLM & NLP
- **LangChain**: LLM application framework
- **OpenAI API**: GPT models
- **Google Gemini API**: Gemini models
- **Sentence Transformers**: Text embeddings
- **Hugging Face**: Model hub

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Poetry**: Python dependency management
- **DevContainer**: VSCode development environment

## File Structure

```
Knowledge-Graph-Construction-using-LLM/
├── app/
│   ├── components/
│   │   ├── chunking.py          # Text chunking utilities
│   │   ├── embedder.py          # Embedding generation
│   │   ├── extractor.py         # LLM-based extraction
│   │   ├── pipeline.py          # Integrated pipeline
│   │   ├── store_neo4j.py       # Neo4j storage
│   │   └── download2csv.py      # CSV export
│   ├── example.py               # Usage example
│   └── main.py                  # CLI application
├── tests/
│   ├── test_components.py       # Component tests
│   └── conftest.py              # Test configuration
├── docs/
│   ├── DOCKER_SETUP.md          # Docker setup guide
│   └── USAGE_GUIDE.md           # Usage documentation
├── scripts/
│   └── quickstart.sh            # Quick start script
├── .devcontainer/
│   └── devcontainer.json        # DevContainer config
├── data/                        # Data directory
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker Compose config
├── pyproject.toml               # Poetry configuration
├── Makefile                     # Convenience commands
├── README.md                    # Main documentation
└── CONTRIBUTING.md              # Contributing guide
```

## Hardware Optimization

### RTX-4080 (8GB VRAM) Optimizations
1. **Memory Management**: `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512`
2. **Batch Sizing**: Optimized batch sizes for 8GB memory
3. **Model Selection**: Lightweight models by default
4. **Cache Management**: Automatic CUDA cache clearing
5. **Shared Memory**: Docker shm-size configuration

## Usage Scenarios

### 1. Academic Research
- Extract entities and relationships from research papers
- Build knowledge graphs of academic concepts
- Analyze citation networks and research trends

### 2. Legal Documents
- Process legal documents and regulations
- Extract legal entities and their relationships
- Special support for Korean law documents

### 3. Business Intelligence
- Extract insights from business documents
- Build organizational knowledge graphs
- Analyze relationships between companies and products

### 4. Content Analysis
- Process news articles and blogs
- Extract topics and named entities
- Build content recommendation systems

## Getting Started

### Quick Start (3 steps)

1. **Setup Environment**
   ```bash
   cp .env.example .env
   # Add your API keys
   ```

2. **Start Services**
   ```bash
   ./scripts/quickstart.sh
   # or: make quickstart
   ```

3. **Run Example**
   ```bash
   docker-compose exec kg-app bash
   poetry install
   poetry run python app/example.py
   ```

### Next Steps
- See `README.md` for detailed documentation
- Check `docs/USAGE_GUIDE.md` for advanced usage
- Read `docs/DOCKER_SETUP.md` for Docker details

## Performance Characteristics

### Processing Speed
- **Small documents** (<1000 words): ~10-30 seconds
- **Medium documents** (1000-5000 words): ~1-3 minutes
- **Large documents** (5000+ words): ~3-10 minutes

*Times vary based on:*
- LLM API latency
- Number of entities/relationships
- Embedding generation (if enabled)
- GPU vs CPU mode

### Resource Usage
- **GPU Memory**: 2-6GB during processing
- **System Memory**: 4-8GB recommended
- **Disk Space**: ~10GB for Docker images + data
- **Network**: LLM API calls require internet

## Limitations and Considerations

1. **API Costs**: LLM API calls incur costs (OpenAI/Google)
2. **Accuracy**: Extraction quality depends on LLM and text quality
3. **Languages**: Best results with English; multilingual support varies
4. **Context**: Large documents may lose context in chunking
5. **Hardware**: GPU recommended but not required (CPU fallback available)

## Future Enhancements

Potential improvements:
- Support for more LLM providers (Anthropic, Cohere)
- Local LLM support (Ollama, llama.cpp)
- Graph visualization tools
- REST API for programmatic access
- Streamlit UI for interactive usage
- Advanced entity resolution and deduplication
- Incremental updates without full reprocessing
- Multi-language support improvements

## Contributing

See `CONTRIBUTING.md` for guidelines on:
- Setting up development environment
- Code style and conventions
- Testing requirements
- Pull request process

## License

MIT License - See LICENSE file for details

## Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: eeariorie@gmail.com

---

**Project Status**: ✅ Production Ready

Last Updated: December 2024
Version: 0.1.0
