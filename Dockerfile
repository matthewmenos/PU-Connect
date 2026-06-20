# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile /app/
# We skip the lock check because Pipfile.lock might be out of sync after manual fixes
RUN pipenv install --system --skip-lock

# Copy project
COPY . /app/

# Run entrypoint script
ENTRYPOINT ["/app/docker/entrypoint.sh"]
