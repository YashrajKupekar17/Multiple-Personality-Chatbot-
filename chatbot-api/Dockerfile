FROM python:3.11-slim

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY uv.lock pyproject.toml README.md ./
RUN uv sync --frozen --no-cache

# Copy your source code
COPY src/mpdagents mpdagents/

# Use uvicorn directly instead of fastapi CLI
CMD ["uv", "run", "uvicorn", "mpdagents.infrastructure.api:app", "--host", "0.0.0.0", "--port", "8000"]
