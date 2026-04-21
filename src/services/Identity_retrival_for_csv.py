import csv
import os
from app import utils
from app.llm import Llm
from components.base_component import BaseComponent
from datalayer.Neo4jDumper import Neo4jDumper


class NameIdentityRetrievalForCsv(BaseComponent):
    def __init__(self, model_name, data_path):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines all its attributes.
        The self parameter refers to an instance of a class, and it's required in order for Python to know which object you're referring to.

        :param self: Represent the instance of the class
        :param model_name: Instantiate the Hugging Face LLM model
        :param data_path: Read the yaml file which contains the path to all csv files
        :return: The instance of the class
        """
        super().__init__('NameIdentityRetrievalForCsv')
        self.sources = utils.read_yaml_file(data_path)
        self.csv_sources = self.sources.get('csv', [])
        # Instantiate the Hugging Face-backed LLM wrapper and Neo4j connection.
        self.neo4j_instance = Neo4jDumper(config_path='app/config.yml')
        self.llm = Llm(model=model_name)

    def run(self, **kwargs):
        """
        The run function is the main function of this module. It takes in a list of csv files and extracts a knowledge graph from them using a Hugging Face model.
        The knowledge graph is then dumped into neo4j database.

        :param self: Represent the instance of the class
        :return: A tuple of the following:
        """
        for csvfile in self.csv_sources:
            # loading the csv using standard csv module
            # Fix path resolution
            if not os.path.exists(csvfile):
                # Try adding src/ prefix if running from root
                if os.path.exists(os.path.join('src', csvfile)):
                    csvfile = os.path.join('src', csvfile)
                else:
                    self.logger.error(f"CSV file not found: {csvfile}")
                    continue

            try:
                rows = []
                # Use latin-1 to avoid utf-8 decode errors
                with open(csvfile, 'r', encoding='latin-1') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        rows.append(row)
                
                if not rows:
                    continue

                # Original logic used data[-1] (last row) - converted to text format
                last_row = rows[-1]
                # Mimic CSVLoader format: "key: value\n..."
                page_content = "\n".join([f"{k}: {v}" for k, v in last_row.items()])

                # Use the configured Hugging Face model and extract knowledge graph.
                self.logger.info(f'loading model {self.llm}')
                
                response = self.llm.run(input_text=page_content)
                # instantiating neo4jBD and dumping the knowledge graph
                self.neo4j_instance.run(data=response)
                self.logger.info(f'knowledge graph populated successfully for data source: {csvfile}')
            except Exception as e:
                self.logger.error(f"Error processing csv {csvfile}: {e}")
