import librosa 
import soundfile as sf 
import os 
import requests 

def test_identification (audio_path :str ):

    y ,sr =librosa .load (audio_path ,offset =10 ,duration =5 )
    temp_query ="test_query.wav"
    sf .write (temp_query ,y ,sr )

    url ="http://localhost:8000/identify"
    with open (temp_query ,"rb")as f :
        response =requests .post (url ,files ={"file":f })

    if response .status_code ==200 :
        print ("Response:",response .json ())
    else :
        print ("Error:",response .text )

    if os .path .exists (temp_query ):
        os .remove (temp_query )

if __name__ =="__main__":

    test_song ="data/raw/data/blues/blues.00000.wav"
    if os .path .exists (test_song ):
        print (f"Testing with {test_song }...")
        test_identification (test_song )
    else :
        print (f"File not found: {test_song }")
