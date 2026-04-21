import sys
import os
import logging
from pathlib import Path

# Add src to path using script location (works from any cwd).
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from services.cypher_qa import CypherQa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_qa():
    model_name = os.getenv("HF_MODEL_ID", "Qwen/Qwen3-30B-A3B-Instruct-2507")
    try:
        qa = CypherQa(model_name=model_name)
    except Exception as e:
        logger.exception("Failed to initialize CypherQa: %s", e)
        return

    questions = [
        "What songs are in the dataset?"
    ]
    
    for q in questions:
        logger.info("Question: %s", q)
        try:
            response = qa.run(q)
            logger.info("Answer: %s", response)
        except Exception as e:
            logger.exception("QA failed: %s", e)

if __name__ == "__main__":
    test_qa()
