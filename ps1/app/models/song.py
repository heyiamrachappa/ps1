from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session, select
import pandas as pd
import os

class Song(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    song_id: str = Field(index=True, unique=True)
    title: str
    artist: str
    duration: float
    genre: Optional[str] = None
    fingerprint_path: Optional[str] = None

class MetadataIngestor:
    def __init__(self, db_url: str = "sqlite:///./audio_id.db"):
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    def ingest_from_csv(self, csv_path: str):
        """Issue 1: Implement Dataset Metadata Ingestion"""
        if not os.path.exists(csv_path):
            print(f"Warning: Metadata file {csv_path} not found.")
            return

        df = pd.read_csv(csv_path)
        with Session(self.engine) as session:
            for _, row in df.iterrows():
                # Check if exists to prevent duplicates
                existing = session.exec(select(Song).where(Song.song_id == str(row['song_id']))).first()
                if existing:
                    continue
                
                song = Song(
                    song_id=str(row['song_id']),
                    title=row['title'],
                    artist=row['artist'],
                    duration=row['duration'],
                    genre=row.get('genre', 'Unknown')
                )
                session.add(song)
            session.commit()
        print(f"Successfully ingested {len(df)} records.")

if __name__ == "__main__":
    # Quick test/initialization
    ingestor = MetadataIngestor()
