import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    from langchain.schema import Document
    logger.info("Found langchain.schema.Document")
except ImportError:
    try:
        from langchain_core.documents import Document
        logger.info("Found langchain_core.documents.Document")
    except ImportError:
        logger.error("Document not found")
