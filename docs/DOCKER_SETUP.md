# Docker Setup Guide

## Prerequisites

1. **Docker and Docker Compose**
   - Install Docker Desktop (Windows/Mac) or Docker Engine (Linux)
   - Verify installation: `docker --version` and `docker-compose --version`

2. **NVIDIA GPU Support (for GPU acceleration)**
   - Install NVIDIA drivers
   - Install NVIDIA Docker Runtime: https://github.com/NVIDIA/nvidia-docker
   - Verify GPU support: `docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi`

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/WB-Jang/Knowledge-Graph-Construction-using-LLM.git
cd Knowledge-Graph-Construction-using-LLM
```

### 2. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Start Services

```bash
# Option 1: Using the quickstart script
./scripts/quickstart.sh

# Option 2: Using Makefile
make quickstart

# Option 3: Using docker-compose directly
docker-compose up -d
```

### 4. Access the Application

```bash
# Enter the application container
docker-compose exec kg-app bash

# Inside the container, install dependencies
poetry install

# Run the example
poetry run python app/example.py
```

## Common Commands

See Makefile for available commands:
```bash
make help
```

## Troubleshooting

### Neo4j Connection Issues
- Wait 10-30 seconds for Neo4j to start
- Check logs: `docker-compose logs neo4j`

### GPU Not Available
- Verify NVIDIA Docker Runtime
- Application will fallback to CPU if GPU unavailable

### Memory Issues (RTX-4080 8GB)
- Reduce batch size
- Use smaller models
- Process fewer chunks

For more details, see the full documentation in the README.md
