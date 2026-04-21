import logging
import sys
from pathlib import Path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


logger.info("Importing langchain")
import langchain
logger.info("Importing pydantic")
import pydantic
logger.info("Pydantic version: %s", pydantic.__version__)

logger.info("Importing Neo4jDumper")
try:
    from datalayer.Neo4jDumper import Neo4jDumper
    logger.info("Neo4jDumper imported")
except Exception as e:
    logger.exception("Neo4jDumper failed: %s", e)

logger.info("Importing Identity_retrival_for_html")
try:
    from services.Identity_retrival_for_html import NameIdentityRetrievalForHtml
    logger.info("NameIdentityRetrievalForHtml imported")
except Exception as e:
    logger.exception("NameIdentityRetrievalForHtml failed: %s", e)

logger.info("Importing Identity_retrival_for_csv")
try:
    from services.Identity_retrival_for_csv import NameIdentityRetrievalForCsv
    logger.info("NameIdentityRetrievalForCsv imported")
except Exception as e:
    logger.exception("NameIdentityRetrievalForCsv failed: %s", e)
