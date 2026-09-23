# Starts the FastAPI backend and the Vite dev server together, each in
# its own new window, and stops when you close them. Run from the repo
# root in PowerShell.
#
# First-time setup (once):
#   py -3.11 -m venv .venv
#   .\.venv\Scripts\Activate.ps1
#   pip install -r requirements.txt
#   Copy-Item .env.example .env      # then add your GROQ_API_KEY
#   cd frontend; npm install; cd ..
#
# Then, every time:
#   .\dev.ps1

if (-not (Test-Path ".env")) {
    Write-Host "No .env found. Copy .env.example to .env and add your GROQ_API_KEY first."
    exit 1
}

Write-Host "Starting API on http://localhost:8000 ..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn api.main:app --reload --port 8000"

Write-Host "Starting frontend on http://localhost:5173 ..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
