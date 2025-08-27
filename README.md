# 10-K Third-Party Risk Graph

An AI-driven app to ingest SEC 10-K filings, extract third-party risks, and visualize them as an interactive graph.

## Quick Start

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm start
```

Frontend runs on http://localhost:3000 and fetches the graph from http://localhost:8000/graph.
