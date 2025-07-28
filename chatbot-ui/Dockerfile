FROM python:3.11-slim

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY uv.lock pyproject.toml README.md ./
RUN uv sync --frozen --no-cache

# Copy your source code
COPY app.py .

# Use uv to run Streamlit
CMD ["/app/.venv/bin/python", "-m", "streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true"]
