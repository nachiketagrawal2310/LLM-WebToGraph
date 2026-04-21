import sys
import os
import logging
import traceback

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from services.Identity_retrival_for_csv import NameIdentityRetrievalForCsv
from app import utils

logging.basicConfig(level=logging.INFO)

def run():
    print("Debug Ingestion FULL Script")
    try:
        # Check if config exists
        if not os.path.exists('src/datalayer/datasources.yml'):
           print("WARNING: src/datalayer/datasources.yml not found in CWD")
        else:
           print("Found src/datalayer/datasources.yml")

        # Instantiate the actual service
        # Note: main.py uses 'datalayer/datasources.yml' 
        # But from root, that path is invalid usually? 
        # Let's try what main.py uses.
        
        # We need to simulate the exact path passed in main.py
        # main.py runs from root.
        
        data_path = 'src/datalayer/datasources.yml' # Adjusted for validity from root
        # Or should I try the broken path? 'datalayer/datasources.yml'
        
        print(f"Using data_path: {data_path}")
        
        ner = NameIdentityRetrievalForCsv(model_name='gemini-2.5-flash', data_path=data_path)
        print("Initialized service.")
        
        print("Running service...")
        ner.run()
        print("Finished run.")
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    run()
