import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add src to path using script location (works from any cwd).
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from app.llm import Llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify():
    load_dotenv(override=True)
    model_name = os.getenv("HF_MODEL_ID", "Qwen/Qwen3-30B-A3B-Instruct-2507")
    logger.info("Using Hugging Face model: %s", model_name)
    
    try:
        logger.info("Initializing Llm with Hugging Face Qwen")
        llm = Llm(model=model_name)
        
        logger.info("Testing extraction with a simple sentence")
        input_text = "Google announced a new data platform in California on December 6, 2023. It aims to improve public service delivery."
        # Note: This relies on the schema.yml being present and valid.
        try:
            result = llm.run(input_text)
            logger.info("Result: %s", result)
            logger.info("Verification SUCCESS")
        except Exception as e:
            logger.warning("Extraction failed: %s", e)
            logger.info("Trying direct generation to confirm connection")
            try:
                msg = llm.llm.invoke("Hello, are you working?")
                logger.info("Direct generation result: %s", msg.content)
                logger.info("Connection SUCCESS (but extraction failed)")
            except Exception as e2:
                logger.exception("Direct generation failed: %s", e2)

    except Exception as e:
        logger.exception("Initialization failed: %s", e)

if __name__ == "__main__":
    verify()
