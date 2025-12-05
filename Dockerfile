# Base image with PyTorch 2.3.0 + CUDA 12.1 + cuDNN 8
# Optimized for RTX-4080 (8GB VRAM)
FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-devel

# Environment variables
ENV NVM_DIR="/home/appuser/.nvm"
ENV PATH="/opt/poetry/bin:/home/appuser/.local/bin:${NVM_DIR}/versions/node/v20.16.0/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

# GPU Memory optimization for RTX-4080 8GB
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
ENV CUDA_VISIBLE_DEVICES=0

# Use bash for subsequent RUN commands
SHELL ["/bin/bash", "-c"]

# Install system dependencies as root
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      git \
      ca-certificates \
      build-essential \
      cmake \
      pkg-config \
      libffi-dev \
      libssl-dev \
      libxml2-dev \
      libxslt1-dev \
      zlib1g-dev \
      libmagic1 \
      libmagic-dev \
      vim \
      nano \
      htop \
      wget \
  && rm -rf /var/lib/apt/lists/*

# Install Rust (for some torch/tokenizer builds) + Poetry
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y \
  && echo 'source "$HOME/.cargo/env"' >> /etc/bash.bashrc \
  && curl -sSL https://install.python-poetry.org | python3 -

# Create non-root user and working directory
RUN useradd --create-home --shell /bin/bash appuser \
  && mkdir -p /app \
  && chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Switch to non-root user
USER appuser

# Install nvm, Node.js (for some utilities)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install 20 && \
    nvm use 20 && \
    nvm alias default 20

# Copy dependency files (for build cache)
COPY --chown=appuser:appuser pyproject.toml poetry.lock* ./

# Install Python dependencies using Poetry
RUN poetry --version \
  && poetry config virtualenvs.create true \
  && poetry config virtualenvs.in-project true \
  && poetry install --no-root --only main --sync --no-interaction

# Set virtual environment paths
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:${PATH}"

# Copy application code
COPY --chown=appuser:appuser . /app

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/models /app/outputs

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Default shell
CMD ["bash"]
