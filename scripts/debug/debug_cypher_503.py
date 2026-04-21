import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path using script location (works from any cwd).
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from services.cypher_qa import CypherQa
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug():
    load_dotenv(override=True)
    model_name = os.getenv("HF_MODEL_ID", "meta-llama/Llama-3.2-1B-Instruct")
    logger.info("Using model: %s", model_name)
    
    try:
        logger.info("Initializing CypherQa")
        qa = CypherQa(model_name=model_name)
        
        question = "what and how is total data"
        logger.info("Running query: %s", question)
        response = qa.run(question)
        logger.info("Response: %s", response)
    except Exception as e:
        logger.exception("Debug failed with: %s", e)

if __name__ == "__main__":
    debug()
