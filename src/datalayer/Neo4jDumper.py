import os
from langchain_neo4j import Neo4jGraph
from langchain_community.graphs.graph_document import GraphDocument
from neo4j import GraphDatabase

from app import utils
from components.base_component import BaseComponent
from datalayer.KnowledgeGraph import map_to_base_node, map_to_base_relationship


class Neo4jDumper(BaseComponent):
    def __init__(self, config_path):
        super().__init__('Neo4jDumper')
        
        # Resolve config path absolutely to avoid CWD issues
        # file is in src/datalayer
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir) # src
        config_path_abs = os.path.join(src_dir, 'app', 'config.yml')
        
        self.logger.info(f"Reading config from {config_path_abs}")
        config = utils.read_yaml_file(config_path_abs)
        
        if not config:
            self.logger.warning("Config not found via absolute path, trying fallback relative paths...")
            config = utils.read_yaml_file('src/app/config.yml')
            if not config:
                 config = utils.read_yaml_file('app/config.yml')
        
        if not config:
            self.logger.error("CRITICAL: Could not find config.yml!")
            raise FileNotFoundError("config.yml not found")

        self.uri = config.get('neo4j', {}).get('uri')
        self.username = config.get('neo4j', {}).get('username')
        self.password = config.get('neo4j', {}).get('password')
        
        if not self.uri:
            raise ValueError("Neo4j URI not configured")

        self.graph = Neo4jGraph(
            url=self.uri, username=self.username, password=self.password
        )

    def dump_data(self, tx, data):
        for key, value in data.items():
            # Create a node for each key-value pair
            tx.run(query="CREATE (n:Node {key: $key, value: $value})", key=key, value=value)
            self.logger.info(f"Dumped data for {key}: {value} to neo4j")

    def run(self, data):
        try:
            with GraphDatabase.driver(self.uri, auth=(self.username, self.password)) as driver:
                with driver.session() as session:
                    self.dump_data(session, data)
            self.logger.info("Neo4j database connected successfully. and data dumped successfully.")
        except Exception as e:
            self.logger.error(f"Error while connecting to neo4j: {str(e)}")
        finally:
            session.close()

    # New implementation using graph document
    def run2(self, data, document):
        try:
            graph = Neo4jGraph(
                url=self.uri, username=self.username, password=self.password
            )
            # Construct a graph document
            graph_document = GraphDocument(
                nodes=[map_to_base_node(node) for node in data.nodes],
                relationships=[map_to_base_relationship(rel) for rel in data.rels],
                source=document
            )
            # Store information into a graph
            graph.add_graph_documents([graph_document])

        except Exception as e:
            self.logger.error(f"Error while connecting to neo4j: {str(e)}")
