from concurrent .futures import ProcessPoolExecutor 
import os 
from sqlmodel import Session ,create_engine ,select 
from app .models .song import Song 
from app .core .features import BaselineFingerprinter ,generate_hashes 
from app .data .store import FingerprintStore 
import time 


BASE_DIR =os .path .dirname (os .path .abspath (__file__ ))
DB_PATH =os .path .join (BASE_DIR ,"audio_id.db")

def process_single_song (song_id ):
    """Worker function for parallel indexing"""

    audio_path =os .path .join (BASE_DIR ,"data/raw",song_id )
    if not os .path .exists (audio_path )and not audio_path .endswith (".wav"):
        audio_path +=".wav"

    if not os .path .exists (audio_path ):
        return None 

    fingerprinter =BaselineFingerprinter ()
    try :
        peaks =fingerprinter .extract (audio_path )
        hashes =generate_hashes (peaks )
        return song_id ,hashes 
    except Exception as e :
        print (f"Error processing {audio_path }: {e }")
        return None 

def index_all ():
    """Issue 4, 10, 15: Parallelized Indexing and Memory Optimization"""
    from sqlmodel import SQLModel 
    engine =create_engine (f"sqlite:///{DB_PATH }")


    SQLModel .metadata .create_all (engine )

    store =FingerprintStore ()

    with Session (engine )as session :
        songs =session .exec (select (Song )).all ()
        song_ids =[s .song_id for s in songs ]
        print (f"Indexing {len (song_ids )} songs using parallel workers...")

        start_total =time .time ()
        with ProcessPoolExecutor ()as executor :
            results =list (executor .map (process_single_song ,song_ids ))

        for res in results :
            if res :
                song_id ,hashes =res 
                store .add_hashes (song_id ,hashes )

    store .save ()
    print (f"Indexing complete in {time .time ()-start_total :.2f}s.")

if __name__ =="__main__":
    index_all ()
