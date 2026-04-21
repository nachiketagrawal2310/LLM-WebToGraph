import logging
import os
import sys
from pathlib import Path

# Add src to path using script location (works from any cwd).
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from services.Identity_retrival_for_csv import NameIdentityRetrievalForCsv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    logger.info("Debug Ingestion FULL Script")
    try:
        model_name = os.getenv("HF_MODEL_ID", "Qwen/Qwen3-30B-A3B-Instruct-2507")
        data_path = REPO_ROOT / "src" / "datalayer" / "datasources.yml"

        if not data_path.exists():
            logger.warning("Datasources file not found: %s", data_path)
        else:
            logger.info("Found datasources file: %s", data_path)

        logger.info("Using data_path: %s", str(data_path))
        ner = NameIdentityRetrievalForCsv(model_name=model_name, data_path=str(data_path))
        logger.info("Initialized service")

        logger.info("Running service")
        ner.run()
        logger.info("Finished run")
    except Exception as e:
        logger.exception("Error while running debug ingestion: %s", e)


if __name__ == "__main__":
    run()
