# 10K Risk Graph Application

## Overview

The **10K Risk Graph** application is a tool designed to help companies analyze **third-party and nth-party risks** based on their SEC 10-K filings. The app extracts risk statements from filings, identifies relationships between the primary company and its third parties, and visualizes these risks in an **interactive network graph**.

This enables **risk analysts, compliance teams, and business stakeholders** to quickly understand exposure and dependencies across their supply chain or partner ecosystem.

---

## Features

### SEC 10-K Ingestion
- Automatically fetch filings via **SEC EDGAR** using a company ticker or CIK.
- Upload text files of filings for **offline processing**.

### Risk Extraction
- Extracts risk-related statements using a **NLP-based extractor**.
- Identifies connections between primary companies, third parties, and specific risk statements.

### Graph Visualization
- Stores relationships in a **graph structure** (nodes = companies/risks, edges = relationships).
- Frontend visualizes the network using **Cytoscape.js**, allowing **interactive exploration**.

### Multi-Party Analysis
- Models **third-party and nth-party relationships**.
- Supports **adding multiple filings over time** to track risk evolution.

---

## Architecture


- **Backend:** FastAPI application handling ingestion, parsing, risk extraction, and providing a REST API.
- **Frontend:** React app using **Cytoscape.js** to visualize the risk network. Communicates with the backend via REST API.

---

## Installation

### 1. Backend

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
# source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload


- **Backend:** FastAPI application handling ingestion, parsing, risk extraction, and providing a REST API.
- **Frontend:** React app using **Cytoscape.js** to visualize the risk network. Communicates with the backend via REST API.
```
---
### 2. Frontend
```bash
cd frontend
npm install
npm start
```

## Usage Examples
Ingest a filing by ticker:
```bash
curl -X POST "http://127.0.0.1:8000/ingest/ticker" \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL"}'
```
Upload a local 10-K text file:
```bash
curl -X POST "http://127.0.0.1:8000/ingest/upload" \
  -F "file=@sample_10k.txt"
```
Retrieve the risk graph:
```bash
curl http://127.0.0.1:8000/graph
```

## Notes and Considerations
SEC Downloader: Requires an email address for polite requests to SEC EDGAR.
CORS: Backend includes CORS middleware for frontend calls from localhost:3000.
Graph Memory: Graph is stored in memory; restarting the backend resets it.
Extensibility: Improve NLP extraction or persist the graph in a database for long-term analysis.

### Future Improvements 🌱

Integrate persistent storage (PostgreSQL, Neo4j) for the risk graph.
Enhance NLP risk extraction using large language models for better accuracy.
Add dashboard filters by risk type, third-party tier, or date.
Enable nth-party automated ingestion to map indirect dependencies.


[10-K Filing] --> [Backend NLP Extraction] --> [Risk Graph DB/Memory]
                                 |
                                 v
                          [Frontend Visualization]




