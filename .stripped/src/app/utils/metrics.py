import time 
import logging 

class LatencyTracker :
    """Issue 13: Establish System Latency Tracking"""
    def __init__ (self ):
        self .logger =logging .getLogger ("latency_tracker")
        logging .basicConfig (level =logging .INFO )

    def log_latency (self ,operation :str ,duration :float ):
        self .logger .info (f"Operation: {operation } | Latency: {duration *1000 :.2f}ms")

class AccuracyEvaluator :
    """Issue 14: Establish Identification Accuracy Metrics"""
    def __init__ (self ):
        self .total =0 
        self .correct =0 

    def record_result (self ,expected :str ,predicted :str ):
        self .total +=1 
        if expected ==predicted :
            self .correct +=1 

    def get_report (self ):
        accuracy =(self .correct /self .total )*100 if self .total >0 else 0 
        return {
        "total_queries":self .total ,
        "correct":self .correct ,
        "accuracy_percent":round (accuracy ,2 )
        }
