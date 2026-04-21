import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Importing AsyncHtmlLoader")
try:
    from langchain_community.document_loaders import AsyncHtmlLoader
    logger.info("AsyncHtmlLoader imported")
except Exception as e:
    logger.exception("AsyncHtmlLoader failed: %s", e)
