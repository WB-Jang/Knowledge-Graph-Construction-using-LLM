#!/bin/bash

# Quick Start Script for Knowledge Graph Construction

set -e

echo "=================================================="
echo "Knowledge Graph Construction - Quick Start"
echo "=================================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ""
    echo "WARNING: Please edit .env file and add your API keys:"
    echo "  - OPENAI_API_KEY (for OpenAI models)"
    echo "  - GOOGLE_API_KEY (for Google Gemini models)"
    echo ""
    read -p "Press Enter to continue after setting up .env file..."
fi

# Start services
echo "Starting Neo4j and application containers..."
docker-compose up -d

echo ""
echo "Waiting for Neo4j to start..."
sleep 10

# Check Neo4j health
echo "Checking Neo4j connection..."
for i in {1..30}; do
    if docker-compose exec -T neo4j cypher-shell -u neo4j -p password123 "RETURN 1" > /dev/null 2>&1; then
        echo "Neo4j is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Error: Neo4j failed to start. Check logs with: docker-compose logs neo4j"
        exit 1
    fi
    echo "Waiting... ($i/30)"
    sleep 2
done

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Services running:"
echo "  - Neo4j: http://localhost:7474 (user: neo4j, password: password123)"
echo "  - Application container: kg-app"
echo ""
echo "Next steps:"
echo ""
echo "1. Enter the application container:"
echo "   docker-compose exec kg-app bash"
echo ""
echo "2. Install dependencies (first time only):"
echo "   poetry install"
echo ""
echo "3. Run the example:"
echo "   poetry run python app/example.py"
echo ""
echo "4. Or process your own data:"
echo "   poetry run python app/main.py --input data/sample.txt --clear-db"
echo ""
echo "=================================================="
