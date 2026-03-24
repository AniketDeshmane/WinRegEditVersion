FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Install additional development tools
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install Python development dependencies
RUN pip install --upgrade pip setuptools wheel

# Note: This project is Windows-specific and uses winreg module
# The dev container is primarily for development, linting, and testing
# The actual functionality (Windows Registry manipulation) requires Windows
