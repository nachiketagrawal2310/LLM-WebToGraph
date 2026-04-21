import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Importing BeautifulSoupTransformer")
try:
    from langchain_community.document_transformers import BeautifulSoupTransformer
    logger.info("BeautifulSoupTransformer imported")
except Exception as e:
    logger.exception("BeautifulSoupTransformer failed: %s", e)

logger.info("Importing CSVLoader")
try:
    from langchain_community.document_loaders import CSVLoader
    logger.info("CSVLoader imported")
except Exception as e:
    logger.exception("CSVLoader failed: %s", e)
