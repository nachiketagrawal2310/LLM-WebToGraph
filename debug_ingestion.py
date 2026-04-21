import sys
import os
import logging
import traceback

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from services.Identity_retrival_for_csv import NameIdentityRetrievalForCsv
from app import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run():
    logger.info("Debug Ingestion FULL Script")
    try:
        model_name = os.getenv("HF_MODEL_ID", "Qwen/Qwen3-30B-A3B-Instruct-2507")
        # Check if config exists
        if not os.path.exists('src/datalayer/datasources.yml'):
           logger.warning("src/datalayer/datasources.yml not found in CWD")
        else:
           logger.info("Found src/datalayer/datasources.yml")

        # Instantiate the actual service
        # Note: main.py uses 'datalayer/datasources.yml' 
        # But from root, that path is invalid usually? 
        # Let's try what main.py uses.
        
        # We need to simulate the exact path passed in main.py
        # main.py runs from root.
        
        data_path = 'src/datalayer/datasources.yml' # Adjusted for validity from root
        # Or should I try the broken path? 'datalayer/datasources.yml'
        
        logger.info("Using data_path: %s", data_path)
        
        ner = NameIdentityRetrievalForCsv(model_name=model_name, data_path=data_path)
        logger.info("Initialized service")
        
        logger.info("Running service")
        ner.run()
        logger.info("Finished run")
        
    except Exception as e:
        logger.exception("Error while running debug ingestion: %s", e)

if __name__ == "__main__":
    run()
