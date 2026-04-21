import sys
import os
import logging
import traceback

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.services.cypher_qa import CypherQa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_qa():
    model_name = os.getenv("HF_MODEL_ID", "Qwen/Qwen3-30B-A3B-Instruct-2507")
    try:
        qa = CypherQa(model_name=model_name)
    except Exception as e:
        logger.error(f"Failed to initialize CypherQa: {e}")
        traceback.print_exc()
        return

    questions = [
        "What songs are in the dataset?"
    ]
    
    for q in questions:
        logger.info(f"Question: {q}")
        try:
            response = qa.run(q)
            logger.info(f"Answer: {response}")
        except Exception as e:
            logger.error(f"QA failed: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    test_qa()
