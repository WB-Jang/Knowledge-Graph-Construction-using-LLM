.PHONY: help build up down restart logs shell install test format lint clean

help: ## Show this help message
	@echo "Knowledge Graph Construction - Available Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d
	@echo "Waiting for Neo4j to be ready..."
	@sleep 10
	@echo "Services are running!"
	@echo "Neo4j Browser: http://localhost:7474"

down: ## Stop all services
	docker-compose down

restart: down up ## Restart all services

logs: ## Show logs from all services
	docker-compose logs -f

logs-neo4j: ## Show Neo4j logs
	docker-compose logs -f neo4j

logs-app: ## Show application logs
	docker-compose logs -f kg-app

shell: ## Enter application container shell
	docker-compose exec kg-app bash

install: ## Install Python dependencies (run inside container)
	poetry install

example: ## Run example script (run inside container)
	poetry run python app/example.py

process-sample: ## Process sample data (run inside container)
	poetry run python app/main.py --input data/sample.txt --clear-db

test: ## Run tests (run inside container)
	poetry run pytest tests/ -v

format: ## Format code with black (run inside container)
	poetry run black app/

lint: ## Lint code with ruff (run inside container)
	poetry run ruff check app/

clean: ## Remove generated files and caches
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf outputs/*.csv logs/*.log

clean-data: ## Remove Neo4j data volumes
	docker-compose down -v
	@echo "Neo4j data volumes removed"

quickstart: ## Quick start - setup and run everything
	./scripts/quickstart.sh

neo4j-query: ## Execute a Cypher query (use QUERY variable)
	docker-compose exec -T neo4j cypher-shell -u neo4j -p password123 "$(QUERY)"

neo4j-browser: ## Open Neo4j browser
	@echo "Opening Neo4j Browser at http://localhost:7474"
	@command -v xdg-open > /dev/null && xdg-open http://localhost:7474 || \
	 command -v open > /dev/null && open http://localhost:7474 || \
	 echo "Please open http://localhost:7474 in your browser"
