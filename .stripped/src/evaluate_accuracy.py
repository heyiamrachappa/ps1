from app .utils .metrics import AccuracyEvaluator 
import requests 
import os 
import json 

def run_evaluation (test_dir :str ,ground_truth :dict ):
    """Issue 14: Evaluate accuracy against a test set"""
    evaluator =AccuracyEvaluator ()
    url ="http://localhost:8000/identify"

    print (f"Starting accuracy evaluation on {len (ground_truth )} samples...")

    for filename ,expected_song_id in ground_truth .items ():
        file_path =os .path .join (test_dir ,filename )
        if not os .path .exists (file_path ):
            continue 

        with open (file_path ,'rb')as f :
            response =requests .post (url ,files ={'file':f })
            if response .status_code ==200 :
                result =response .json ()
                predicted =result ['result']['best_match']
                evaluator .record_result (expected_song_id ,predicted )
                print (f"File: {filename } | Expected: {expected_song_id } | Predicted: {predicted }")
            else :
                print (f"Failed to identify {filename }: {response .text }")

    report =evaluator .get_report ()
    print ("\n--- Evaluation Report ---")
    print (json .dumps (report ,indent =2 ))

if __name__ =="__main__":


    print ("Please ensure the FastAPI server is running before executing evaluation.")
