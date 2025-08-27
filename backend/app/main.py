from fastapi import FastAPI, UploadFile, File
from .graph import GRAPH_DB, merge_into_graph
from .extractor import extract_risks_from_text
import uvicorn
import os, json, requests
from sec_edgar_downloader import Downloader
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="10K Third-Party Risk Extractor")

dl = Downloader("sec_data", "helen.ristov@gmail.com")

class TickerRequest(BaseModel):
    ticker: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load ticker-to-CIK mapping from SEC
def load_ticker_map():
    url = "https://www.sec.gov/files/company_tickers.json"
    resp = requests.get(url, headers={"User-Agent": "MyApp helen.ristov@gmail.com"})
    data = resp.json()
    mapping = {}
    for entry in data.values():
        mapping[entry["ticker"].upper()] = str(entry["cik_str"]).zfill(10)
    return mapping

TICKER_MAP = load_ticker_map()

@app.post("/ingest/upload")
async def ingest_upload(file: UploadFile = File(...)):
    raw = await file.read()
    text = raw.decode(errors="ignore")
    chunks = text.split("\n\n")
    for c in chunks:
        extracted = extract_risks_from_text(c)
        merge_into_graph(extracted)
    return {"status": "ok"}

@app.post("/ingest/cik")
async def ingest_cik(cik: str):
    try:
        # Download all 10-K filings for the company
        dl.get("10-K", cik)
    except Exception as e:
        return {"status": "download failed", "error": str(e)}

    # Locate the downloaded filings
    filing_dir = os.path.join("sec_data", "sec-edgar-filings", cik, "10-K")
    if not os.path.exists(filing_dir) or len(os.listdir(filing_dir)) == 0:
        return {"status": "no filings found"}

    # Pick the latest filing folder
    latest_folder = sorted(os.listdir(filing_dir))[-1]
    filing_path = os.path.join(filing_dir, latest_folder, "full-submission.txt")

    # Read the filing text
    try:
        with open(filing_path, "r", errors="ignore") as f:
            text = f.read()
    except Exception as e:
        return {"status": "failed to read filing", "error": str(e)}

    # Split into chunks and extract risks
    chunks = text.split("\n\n")
    for c in chunks:
        try:
            extracted = extract_risks_from_text(c)
            merge_into_graph(extracted)
        except Exception as e:
            print("Extraction error:", e)

    return {"status": "ok", "cik": cik}

@app.post("/ingest/ticker")
async def ingest_ticker(req: TickerRequest):
    ticker = req.ticker.upper()
    if ticker not in TICKER_MAP:
        return {"status": "ticker not found"}
    cik = TICKER_MAP[ticker]
    return await ingest_cik(cik)

@app.get("/graph")
async def get_graph():
    return GRAPH_DB

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
