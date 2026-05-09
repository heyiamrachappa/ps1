import os 
import pandas as pd 

def generate_metadata (data_dir :str ):
    rows =[]

    for genre in os .listdir (data_dir ):
        genre_path =os .path .join (data_dir ,genre )
        if os .path .isdir (genre_path ):
            for file in os .listdir (genre_path ):
                if file .endswith (".wav"):
                    song_id =file .replace (".wav","")
                    rows .append ({
                    "song_id":f"data/{genre }/{file }",
                    "title":song_id ,
                    "artist":"Various",
                    "duration":30.0 ,
                    "genre":genre 
                    })

    df =pd .DataFrame (rows )
    df .to_csv ("metadata.csv",index =False )
    print (f"Generated metadata.csv with {len (df )} entries.")

if __name__ =="__main__":
    generate_metadata ("data/raw/data")
