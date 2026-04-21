import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from services.cypher_qa import CypherQa
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug():
    load_dotenv(override=True)
    model_name = os.getenv("HF_MODEL_ID", "meta-llama/Llama-3.2-1B-Instruct")
    logger.info(f"Using model: {model_name}")
    
    try:
        logger.info("Initializing CypherQa")
        qa = CypherQa(model_name=model_name)
        
        question = "what and how is total data"
        logger.info(f"Running query: {question}")
        response = qa.run(question)
        logger.info(f"Response: {response}")
    except Exception as e:
        logger.exception(f"Debug failed with: {e}")

if __name__ == "__main__":
    debug()
