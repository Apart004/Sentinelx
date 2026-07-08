# Base image — slim variant keeps the container small
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency definition first (layer caching — if pyproject.toml doesn't change,
# Docker reuses the cached pip install layer instead of reinstalling everything)
COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Copy the rest of the source code
COPY . .

# Default command — runs when container starts
CMD ["python", "-m", "sentinelx"]