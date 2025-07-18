# syntax=docker/dockerfile:1

FROM python:3.10-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency installation
RUN pip install --no-cache-dir uv

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN uv pip install --no-cache-dir -r requirements.txt

# Default command shows CLI help
CMD ["python", "src/clean_debate_audio.py", "-h"]
