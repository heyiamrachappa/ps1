# Zerograde Audio Identification System

Welcome to the Zerograde Audio ID project. This repository has been reorganized for better clarity.

## Project Structure

- **[docs/](./docs/)**: Contains all project documentation.
  - [Technical Overview](./docs/technical_overview.md): Core architecture and team info.
  - [Architecture Details](./docs/architecture.md): Deep dive into the hybrid feature extraction.
  - [Issue Tracking](./docs/ISSUES.md): Historical and current project issues.
- **[src/](./src/)**: Contains all development source code and runtime data.
  - `app/`: Core logic (models, features, data store).
  - `main.py`: The FastAPI application entry point.
  - `data/`: Raw audio and fingerprint storage.
  - `static/`: Frontend assets.

## Quick Start

### 1. Installation
```bash
pip install -e .
```

### 2. Running the Application
From the project root:
```bash
python src/main.py
```

### 3. Documentation
For detailed setup and execution instructions, please refer to the [Technical Overview](./docs/technical_overview.md).
