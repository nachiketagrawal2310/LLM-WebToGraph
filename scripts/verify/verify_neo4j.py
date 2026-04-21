import os
import sys
import logging
from pathlib import Path

# Add src to path using script location (works from any cwd).
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from app import utils
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_neo4j():
    try:
        logger.info("Reading config")
        config = utils.read_yaml_file(str(REPO_ROOT / 'src' / 'app' / 'config.yml'))
        if not config:
            logger.warning("Config not found in src/app/config.yml, trying app/config.yml")
            config = utils.read_yaml_file(str(REPO_ROOT / 'app' / 'config.yml'))
        
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
