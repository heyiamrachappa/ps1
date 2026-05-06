from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models.song import Song, MetadataIngestor
from app.core.features import BaselineFingerprinter, generate_hashes
from app.data.store import FingerprintStore, MatchingEngine
from app.utils.metrics import LatencyTracker
import shutil
import os
import uuid
import time

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="Zerograde Audio ID System")

# Get absolute path to the directory where main.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Create static directory if not exists
os.makedirs(STATIC_DIR, exist_ok=True)

# Initialize components
store = FingerprintStore()
engine = MatchingEngine(store)
fingerprinter = BaselineFingerprinter()
tracker = LatencyTracker()

@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            return f.read()
    return f"<h1>Zerograde Audio ID System</h1><p>Frontend files missing at {index_path}</p>"

# Mount static files for CSS/JS
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.post("/identify")
async def identify_audio(file: UploadFile = File(...)):
    """Issue 5 & 10: Query Ingestion and Concurrent Handling"""
    start_time = time.time()
    
    # Use a unique extension based on content type if possible, or default to webm
    ext = ".webm" if "webm" in file.content_type else ".wav"
    temp_path = os.path.join(STATIC_DIR, f"temp_{uuid.uuid4()}{ext}")
    
    print(f"Incoming query: {file.filename} ({file.content_type})")
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        if os.path.getsize(temp_path) < 500:
             raise HTTPException(status_code=400, detail="Audio file too short or invalid")

        print(f"Extracting features from {temp_path}...")
        peaks = fingerprinter.extract(temp_path)
        query_hashes = generate_hashes(peaks)
        
        print(f"Matching {len(query_hashes)} hashes against index...")
        result = engine.match(query_hashes)
        
        latency = time.time() - start_time
        tracker.log_latency("identify", latency)
        
        print(f"Identification complete. Result: {result['best_match']} ({result['confidence']}%)")
        
        return {
            "result": result,
            "latency_ms": round(latency * 1000, 2)
        }
    except Exception as e:
        # Issue 12: Robust error handling
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/health")
async def health_check():
    """Issue 18: Health and Status Checks"""
    return {
        "status": "online",
        "dataset_size": len(store.table),
        "timestamp": time.time()
    }

@app.post("/ingest")
async def ingest_dataset(csv_path: str):
    """Admin endpoint to trigger ingestion"""
    ingestor = MetadataIngestor()
    ingestor.ingest_from_csv(csv_path)
    return {"message": "Ingestion started (check logs for progress)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
