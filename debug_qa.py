import sys
import os
import time
import signal
import traceback

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

import logging
logging.basicConfig(level=logging.DEBUG)

def handler(signum, frame):
    raise TimeoutError("Timeout reached")

signal.signal(signal.SIGALRM, handler)
signal.alarm(60) # 60 seconds timeout

def run():
    print("Debug script starting...")
    try:
        from services.cypher_qa import CypherQa
        print("Imported CypherQa")
        
        print("Instantiating CypherQa...")
        start = time.time()
        qa = CypherQa('gemini-2.5-flash')
        print(f"Instantiated in {time.time() - start:.2f}s")
        
        query = "tell me about yourself"
        print(f"Sending query: '{query}'")
        
        start = time.time()
        result = qa.run(query)
        print(f"Result Type: {type(result)}")
        print(f"Result (took {time.time() - start:.2f}s): {result}")
        
    except Exception as e:
        print(f"EXCEPTION: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    run()
