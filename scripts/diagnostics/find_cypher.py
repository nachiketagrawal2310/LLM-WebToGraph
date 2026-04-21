import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    from langchain.chains import GraphCypherQAChain
    logger.info("Found in langchain.chains")
except ImportError:
    pass

try:
    from langchain_community.chains import GraphCypherQAChain
    logger.info("Found in langchain_community.chains")
except ImportError:
    pass

try:
    from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
    logger.info("Found in langchain_community.chains.graph_qa.cypher")
except ImportError:
    pass
