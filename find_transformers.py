import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    from langchain_community.document_transformers import BeautifulSoupTransformer
    logger.info("Found in langchain_community.document_transformers")
except ImportError:
    logger.warning("Not found in langchain_community.document_transformers")

try:
    from langchain.document_transformers import BeautifulSoupTransformer
    logger.info("Found in langchain.document_transformers")
except ImportError:
    pass
