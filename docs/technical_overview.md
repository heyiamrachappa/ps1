# Audio Identification & Source Detection System

## Project Overview
This project provides a robust, high-performance solution for identifying short audio snippets (3-10 seconds) within a large database of music. It is specifically designed to handle background noise and typical audio distortions encountered in real-world scenarios.

## Team Information
- **Team Name**: Zerograde
- **Project Scope**: Automated Audio Recognition

## Implementation Justification

### Why Landmark Fingerprinting?
We chose a **Landmark-based Fingerprinting** approach (similar to industry standards like Shazam) because it is computationally efficient and highly resistant to background noise. By focusing on the strongest spectral peaks, the system "ignores" low-level noise that doesn't form a constellation.

### Why Mel-Frequency Spectral Analysis?
The system utilizes **Mel-Spectrograms** instead of linear spectrograms. The Mel scale better approximates human hearing and provides more robust frequency binning, making the resulting fingerprints less sensitive to minor frequency fluctuations.

### Why Temporal Alignment?
Instead of just counting matching hashes, our system performs **Temporal Alignment**. It verifies that the matching landmarks in the query appear at the same relative time offsets as they do in the original track. This virtually eliminates false positives.

### Why Parallel Indexing?
Generating fingerprints for thousands of songs can be time-consuming. We implemented a **multi-process indexing pipeline** using Python's `ProcessPoolExecutor`. This allows us to utilize all available CPU cores, reducing the total indexing time by up to 80% on modern hardware.

### Why a Web Interface?
To make the system accessible to non-technical users, we've included a **FastAPI-powered web interface**. It provides a simple drag-and-drop area for audio files, real-time identification progress, and visual feedback for the matching results.

## Setup and Execution Instructions

### 1. Prerequisites
- Python 3.10+
- `ffmpeg` (required for audio processing)

### 2. Installation
```bash
pip install -e .
```

### 3. Data Preparation
1. Organize your audio files (`.wav`) in `src/data/raw/`.
2. Generate the metadata manifest:
   ```bash
   python src/generate_metadata.py
   ```
   This creates `metadata.csv` based on your folder structure.

### 4. System Initialization
First, start the FastAPI server:
```bash
python src/main.py
```

Then, ingest the metadata and index the dataset:
```bash
# Ingest metadata into SQLite
curl -X POST "http://localhost:8000/ingest?csv_path=metadata.csv"

# Build the fingerprint index (CPU-parallelized)
python src/index_dataset.py
```

### 5. Running Queries
- **Web Interface**: Open `http://localhost:8000` in your browser.
- **CLI**:
  ```bash
  curl -X POST "http://localhost:8000/identify" -F "file=@path/to/query.wav"
  ```

### 6. Performance & Evaluation
- **Health Check**: `GET /health` returns system status and index size.
- **Accuracy Test**: Run `python src/evaluate_accuracy.py` to benchmark the system against a labeled test set.

---
**Note:** This documentation is aligned with the codebase as of May 2026. Any changes to the core algorithms should be reflected here immediately.
