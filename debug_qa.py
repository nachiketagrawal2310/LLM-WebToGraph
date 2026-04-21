import sys
import os
import time
import signal
import traceback

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def handler(signum, frame):
    raise TimeoutError("Timeout reached")

signal.signal(signal.SIGALRM, handler)
signal.alarm(60) # 60 seconds timeout

def run():
    logger.info("Debug script starting")
    try:
        from services.cypher_qa import CypherQa
        logger.info("Imported CypherQa")
        model_name = os.getenv("HF_MODEL_ID", "Qwen/Qwen3-30B-A3B-Instruct-2507")
        
        logger.info("Instantiating CypherQa")
        start = time.time()
        qa = CypherQa(model_name)
        logger.info("Instantiated in %.2fs", time.time() - start)
        
        query = "tell me about yourself"
        logger.info("Sending query: '%s'", query)
        
        start = time.time()
        result = qa.run(query)
        logger.info("Result Type: %s", type(result))
        logger.info("Result (took %.2fs): %s", time.time() - start, result)
        
    except Exception as e:
        logger.exception("Exception while running debug QA: %s", e)

if __name__ == "__main__":
    run()
