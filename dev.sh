#!/usr/bin/env bash
# Starts the FastAPI backend and the Vite dev server together, in one
# terminal, and stops both when you Ctrl+C. Run from the repo root.
#
# First-time setup (once):
#   python -m venv .venv && source .venv/bin/activate
#   pip install -r requirements.txt
#   cp .env.example .env            # then add your GROQ_API_KEY
#   cd frontend && npm install && cd ..
#
# Then, every time:
#   ./dev.sh

set -e

if [ ! -f .env ]; then
  echo "No .env found. Copy .env.example to .env and add your GROQ_API_KEY first."
  exit 1
fi

cleanup() {
  echo ""
  echo "Stopping..."
  kill $(jobs -p) 2>/dev/null
}
trap cleanup EXIT INT TERM

echo "Starting API on http://localhost:8000 ..."
uvicorn api.main:app --reload --port 8000 &

echo "Starting frontend on http://localhost:5173 ..."
(cd frontend && npm run dev) &

wait
