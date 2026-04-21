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
        root_dir = os.path.dirname(src_dir) # project root
        
        # Try multiple potential paths for config.yml
        config_paths = [
            os.path.join(src_dir, 'app', 'config.yml'),
            os.path.join(root_dir, 'config.yml'),
            'src/app/config.yml',
            'app/config.yml'
        ]
        
        config = None
        for path in config_paths:
            print(f"DEBUG: Trying config path: {path}")
            self.logger.info(f"Trying to read config from {path}")
            config = utils.read_yaml_file(path)
            if config:
                print(f"DEBUG: Found config at {path}")
                break
        
        if not config:
            print("DEBUG: No config found!")
            self.logger.error("CRITICAL: Could not find config.yml!")
            raise FileNotFoundError("config.yml not found")

        self.uri = config.get('neo4j', {}).get('uri')
        self.username = config.get('neo4j', {}).get('username')
        self.password = config.get('neo4j', {}).get('password')
        self.database = config.get('neo4j', {}).get('database', 'neo4j')
        
        if not self.uri:
            raise ValueError("Neo4j URI not configured")

        try:
            self.graph = Neo4jGraph(
                url=self.uri, username=self.username, password=self.password, database=self.database
            )
            self.logger.info(f"Neo4jGraph initialized successfully for database: {self.database}")
            print(f"DEBUG: Neo4jGraph initialized successfully for database: {self.database}")
        except Exception as e:
            self.logger.error(f"Failed to initialize Neo4jGraph: {e}")
            print(f"DEBUG: Failed to initialize Neo4jGraph: {e}")
            self.graph = None

    def dump_graph(self, tx, knowledge_graph):
        """
        Dumps a KnowledgeGraph object into Neo4j using MERGE.
        """
        if not hasattr(knowledge_graph, 'nodes') or not hasattr(knowledge_graph, 'rels'):
             self.logger.warning("Data is not a valid KnowledgeGraph object.")
             return

        # 1. Create Nodes
        for node in knowledge_graph.nodes:
            base_node = map_to_base_node(node)
            label = base_node.type
            # Sanitize label for Cypher
            safe_label = "".join(c for c in label if c.isalnum() or c == '_')
            if not safe_label: safe_label = "Entity"
            
            query = (
                f"MERGE (n:{safe_label} {{id: $id}}) "
                "SET n += $props "
                "RETURN n"
            )
            try:
                tx.run(query, id=base_node.id, props=base_node.properties)
            except Exception as e:
                self.logger.error(f"Error merging node {base_node.id}: {e}")

        # 2. Create Relationships
        for rel in knowledge_graph.rels:
            base_rel = map_to_base_relationship(rel)
            source_label = "".join(c for c in base_rel.source.type if c.isalnum() or c == '_')
            target_label = "".join(c for c in base_rel.target.type if c.isalnum() or c == '_')
            rel_type = "".join(c for c in base_rel.type if c.isalnum() or c == '_').upper()
            
            if not source_label: source_label = "Entity"
            if not target_label: target_label = "Entity"
            if not rel_type: rel_type = "RELATED_TO"

            query = (
                f"MATCH (s:{source_label} {{id: $source_id}}) "
                f"MATCH (t:{target_label} {{id: $target_id}}) "
                f"MERGE (s)-[r:{rel_type}]->(t) "
                "SET r += $props "
                "RETURN r"
            )
            try:
                tx.run(query, 
                       source_id=base_rel.source.id, 
                       target_id=base_rel.target.id, 
                       props=base_rel.properties)
            except Exception as e:
                self.logger.error(f"Error merging relationship {rel_type}: {e}")

    def run(self, data):
        """
        Main entry point for dumping data. Supports both dict (legacy) and KnowledgeGraph.
        """
        if not self.uri:
            self.logger.error("Neo4j URI not configured, cannot run.")
            return

        try:
            with GraphDatabase.driver(self.uri, auth=(self.username, self.password)) as driver:
                with driver.session(database=self.database) as session:
                    if hasattr(data, 'nodes'):
                        session.execute_write(self.dump_graph, data)
                    elif isinstance(data, dict):
                        # Legacy support
                        session.execute_write(self.dump_data, data)
                    else:
                        self.logger.warning(f"Unsupported data type for dumping: {type(data)}")
            self.logger.info("Data dumped to Neo4j successfully.")
        except Exception as e:
            self.logger.error(f"Error while connecting to neo4j: {str(e)}")

    def dump_data(self, tx, data):
        """Legacy support for flat dictionary dumping."""
        # ... logic moved from earlier session ... (rest preserved or updated)
        properties = {k.replace(' ', '_').replace('/', '_'): v for k, v in data.items() if v and v != 'Unknown' and v != 'None'}
        if not properties: return
        label = properties.get('Project_Name', 'Extraction').replace(' ', '_').replace('/', '_')
        if not label or label == 'Extraction': label = 'Project'
        query = f"MERGE (n:{label} {{Project_Name: $Project_Name}}) SET n += $props RETURN n"
        tx.run(query, Project_Name=data.get('Project_Name', 'Unknown'), props=properties)
