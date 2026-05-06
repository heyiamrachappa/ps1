# Audio Identification & Source Detection System

## Team Information
- **Team Name**: Zerograde
- **Year**: 2nd year
- **All-Female Team**: No

## Architecture Overview

    - **Hybrid Feature Extraction**: We utilize a dual-path approach. **Acoustic Fingerprinting** (landmark-based hashing) captures precise spectral peaks for high accuracy, while **Deep Embeddings** (via VGGish/AST models) are stored in a Vector Database (FAISS/ChromaDB) to provide robustness against extreme distortion and pitch shifts.
    - **Matching Algorithm**: Our system employs a Weighted Fusion technique. It combines hash-based exact matches with **Cosine Similarity** search in the embedding space. A temporal alignment check ensures that the identified snippet follows the correct chronological sequence of the original track.
    - **Scalability**: By using **HNSW indexing** for vector search and **Key-Value stores** for fingerprints, the system achieves $O(\log N)$ and $O(1)$ lookup times respectively. This allows us to handle thousands of songs and concurrent queries with sub-second latency.
    - **Robustness Mechanisms**: Pre-indexing includes **Spectral Subtraction** for denoising and normalization. Our fingerprinting algorithm specifically ignores low-magnitude noise by focusing on dominant spectral constellations, ensuring high confidence even in 3-10 second noisy clips.

**Note:** Please do not change the format or spelling of anything in this README. The fields are extracted using a script, so any changes to the structure or formatting may break the extraction process.

## Setup and Execution Instructions

### 1. Prerequisites
- Python 3.10+
- `ffmpeg` (required for `pydub` and `librosa`)

### 2. Installation
```bash
pip install -e .
```

### 3. Data Preparation
1. Place your raw audio files (`.wav`) in `data/raw/`.
2. Create a `metadata.csv` with columns: `song_id, title, artist, duration, genre`.

### 4. Ingestion & Indexing
First, start the application to initialize the database:
```bash
python main.py
```
Then, in a separate terminal, run the ingestion and indexing scripts:
```bash
# Ingest metadata
curl -X POST "http://localhost:8000/ingest?csv_path=metadata.csv"

# Build the fingerprint index
python index_dataset.py
```

### 5. Running Queries
To identify an audio clip:
```bash
curl -X POST "http://localhost:8000/identify" -F "file=@path/to/your/query.wav"
```

### 6. Health & Metrics
- Health Check: `GET /health`
- Accuracy Evaluation: `python evaluate_accuracy.py`
