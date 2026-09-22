# Restructura One — API backend
# Build/run from the REPO ROOT (not from api/), so core/ and data/ are
# available inside the image:
#   docker build -f api/Dockerfile -t restructura-api .
#   docker run -p 8000:8000 --env-file .env restructura-api

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
COPY api/requirements.txt ./api-requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r api-requirements.txt

COPY . .

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
