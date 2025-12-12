FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for building packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Filter out problematic packages (Windows-only and spaCy models)
# Install filtered requirements
RUN sed -e '/^win-inet-pton/d' -e '/^en-core-web/d' requirements.txt > requirements-docker.txt && \
    pip install --no-cache-dir -r requirements-docker.txt

# Download spaCy English model (can't install via pip)
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
