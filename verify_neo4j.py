import os
import sys
import logging

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from app import utils
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_neo4j():
    try:
        logger.info("Reading config")
        config = utils.read_yaml_file('src/app/config.yml')
        if not config:
            logger.warning("Config not found in src/app/config.yml, trying app/config.yml")
            config = utils.read_yaml_file('app/config.yml')
        
        if not config:
            logger.error("Could not find config.yml")
            return

        uri = config.get('neo4j').get('uri')
        username = config.get('neo4j').get('username')
        password = config.get('neo4j').get('password')
        
        logger.info("Connecting to %s as %s", uri, username)
        
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            with driver.session() as session:
                result = session.run("RETURN 1 AS result")
                record = result.single()
                logger.info("Connection SUCCESS! Result: %s", record['result'])
                
    except Exception as e:
        logger.exception("Connection FAILED: %s", e)

if __name__ == "__main__":
    verify_neo4j()
