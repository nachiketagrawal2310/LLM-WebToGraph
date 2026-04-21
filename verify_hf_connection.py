import os
import sys
import logging
from dotenv import load_dotenv

# Add src to path so we can import app modules
sys.path.append(os.path.join(os.getcwd(), 'src'))

from app.llm import Llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify():
    load_dotenv()
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
