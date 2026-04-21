import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from app import utils
from neo4j import GraphDatabase

def verify_neo4j():
    try:
        print("Reading config...")
        config = utils.read_yaml_file('src/app/config.yml')
        if not config:
            print("Config not found in src/app/config.yml, trying app/config.yml")
            config = utils.read_yaml_file('app/config.yml')
        
        if not config:
            print("ERROR: Could not find config.yml")
            return

        uri = config.get('neo4j').get('uri')
        username = config.get('neo4j').get('username')
        password = config.get('neo4j').get('password')
        
        print(f"Connecting to {uri} as {username}...")
        
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            with driver.session() as session:
                result = session.run("RETURN 1 AS result")
                record = result.single()
                print(f"Connection SUCCESS! Result: {record['result']}")
                
    except Exception as e:
        print(f"Connection FAILED: {e}")

if __name__ == "__main__":
    verify_neo4j()
