import requests
from typing import Union, List
from langchain_core.documents import Document
from langchain_community.document_transformers import BeautifulSoupTransformer
from app import utils
from app.llm import Llm
from components.base_component import BaseComponent
from datalayer.Neo4jDumper import Neo4jDumper


class NameIdentityRetrievalForHtml(BaseComponent):
    def __init__(self, model_name, data_path):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the initial values of all attributes for an instance of a class.
        The self parameter refers to the current instance of a class, and it's required by Python.

        :param self: Represent the instance of the class
        :param model_name: Specify the model name that we want to use for our predictions
        :param data_path: Read the yaml file which contains the links to be scraped
        :return: Nothing
        """
        super().__init__('NameIdentityRetrievalForHtml')
        self.sources = utils.read_yaml_file(data_path)
        self.html_sources = self.sources.get('link', [])
        # Instantiate the Hugging Face-backed LLM wrapper and Neo4j connection.
        self.neo4j_instance = Neo4jDumper(config_path='app/config.yml')
        self.llm = Llm(model=model_name)

    def run_async(self, **kwargs):

        """
        The run_async function is used to run the pipeline asynchronously.
            It takes in a list of html sources and extracts knowledge graph from them using a Hugging Face model.
            The extracted knowledge graph is then dumped into neo4j database.

        :param self: Represent the instance of the object itself
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A list of all the knowledge graphs extracted from the html sources
        """
        for link in self.html_sources:
            try:
                self.logger.info(f"Fetching {link}...")
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = requests.get(link, headers=headers, timeout=30)
                if response.status_code != 200:
                    self.logger.error(f"Failed to fetch {link}: {response.status_code}")
                    continue
                
                html_content = response.text
                doc = Document(page_content=html_content, metadata={"source": link})
                
                # html = loader.load()
                bs_transformer = BeautifulSoupTransformer()
                # transform_documents expects a sequence (list)
                # Expand tags to extract more content
                docs_transformed = bs_transformer.transform_documents([doc], tags_to_extract=["p", "div", "span", "h1", "h2", "h3", "table", "li"])
                
                if not docs_transformed:
                    self.logger.info(f"No content extracted from {link}")
                    continue

                content = docs_transformed[0].page_content
                self.logger.info(f"Content length: {len(content)}")

                # Document spliting
                from langchain_text_splitters import RecursiveCharacterTextSplitter
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1500,
                    chunk_overlap=150,
                    length_function=len,
                )
                chunks = text_splitter.split_text(content)
                self.logger.info(f"Split content into {len(chunks)} chunks.")

                # Use the configured Hugging Face model and extract knowledge graph.
                self.logger.info(f'Processing chunks with model {self.llm}')

                for i, chunk in enumerate(chunks):
                    self.logger.info(f"Processing chunk {i+1}/{len(chunks)}...")
                    # Add schema context for unstructured dataset tracking
                    rich_chunk = f"Source URL: {link}\n\nUnstructured Content:\n{chunk}"
                    
                    # Extract partial knowledge graph from chunk
                    llm_response = self.llm.run(input_text=rich_chunk)
                    
                    # Dump the partial graph to Neo4j
                    self.neo4j_instance.run(data=llm_response)
                
                self.logger.info(f'Knowledge graph populated successfully for data source: {link}')
            except Exception as e:
                self.logger.error(f"Error processing {link}: {e}")

    def run(self, input: Union[str, List[float]]) -> str:
        pass
