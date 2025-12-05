# Contributing to Knowledge Graph Construction using LLM

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Development Setup

### 1. Clone and Setup

```bash
git clone https://github.com/WB-Jang/Knowledge-Graph-Construction-using-LLM.git
cd Knowledge-Graph-Construction-using-LLM
```

### 2. Using DevContainer (Recommended)

The easiest way to develop is using VSCode DevContainer:

1. Install VSCode and Docker
2. Install "Dev Containers" extension
3. Open project in VSCode
4. Press `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

### 3. Manual Setup

```bash
# Start services
docker-compose up -d

# Enter container
docker-compose exec kg-app bash

# Install dependencies
poetry install
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write clean, documented code
- Follow existing code style
- Add tests for new features

### 3. Format and Lint

```bash
# Format code
poetry run black app/

# Lint code
poetry run ruff check app/

# Or use Makefile
make format
make lint
```

### 4. Run Tests

```bash
poetry run pytest tests/ -v

# Or use Makefile
make test
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: your feature description"
```

Use conventional commit messages:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Build process or auxiliary tool changes

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

### Python

- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use type hints where appropriate
- Write docstrings for all public functions/classes

Example:

```python
def process_text(text: str, chunk_size: int = 1000) -> List[str]:
    """
    Process and chunk text.
    
    Args:
        text: Input text to process
        chunk_size: Maximum size of each chunk
        
    Returns:
        List of text chunks
    """
    # Implementation
    pass
```

### Documentation

- Write clear, concise documentation
- Include code examples
- Update README if adding new features
- Add docstrings to all functions

## Testing

### Writing Tests

Place tests in the `tests/` directory:

```python
def test_my_feature():
    """Test description"""
    # Arrange
    input_data = "test"
    
    # Act
    result = my_function(input_data)
    
    # Assert
    assert result == expected_output
```

### Running Tests

```bash
# All tests
poetry run pytest tests/ -v

# Specific test file
poetry run pytest tests/test_components.py -v

# With coverage
poetry run pytest tests/ --cov=app --cov-report=html
```

## Adding New Features

### 1. New Component

1. Create file in `app/components/`
2. Add imports to `app/components/__init__.py`
3. Write tests in `tests/`
4. Update documentation

### 2. New LLM Provider

To add a new LLM provider:

1. Update `LLMExtractor` in `app/components/extractor.py`
2. Add new model type to command-line arguments
3. Update documentation
4. Add tests

### 3. New Storage Backend

To add a new storage backend:

1. Create new module in `app/components/`
2. Implement same interface as `Neo4jStorage`
3. Update `KnowledgeGraphPipeline`
4. Add tests and documentation

## Questions?

Feel free to:
- Open an issue on GitHub
- Contact the maintainers
- Join discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
