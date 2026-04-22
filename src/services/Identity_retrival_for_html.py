import os
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
        # Combine remote URLs and local html file paths into one list
        self.html_sources = self.sources.get('link', []) + self.sources.get('html_file', [])
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
        for source in self.html_sources:
            try:
                # Resolve local file paths (try with 'src/' prefix if needed)
                resolved_path = None
                if not source.startswith('http://') and not source.startswith('https://'):
                    if os.path.exists(source):
                        resolved_path = source
                    elif os.path.exists(os.path.join('src', source)):
                        resolved_path = os.path.join('src', source)
                    else:
                        self.logger.error(f"Local HTML file not found: {source}")
                        continue

                if resolved_path:
                    # Local HTML file
                    self.logger.info(f"Reading local HTML file: {resolved_path}")
                    with open(resolved_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    label = f"file://{os.path.abspath(resolved_path)}"
                else:
                    # Remote URL
                    self.logger.info(f"Fetching {source}...")
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    response = requests.get(source, headers=headers, timeout=30)
                    if response.status_code != 200:
                        self.logger.error(f"Failed to fetch {source}: {response.status_code}")
                        continue
                    html_content = response.text
                    label = source

                doc = Document(page_content=html_content, metadata={"source": label})

                bs_transformer = BeautifulSoupTransformer()
                # Expand tags to extract more content
                docs_transformed = bs_transformer.transform_documents(
                    [doc],
                    tags_to_extract=["p", "div", "span", "h1", "h2", "h3", "h4", "table", "td", "th", "li"]
                )

                if not docs_transformed:
                    self.logger.info(f"No content extracted from {label}")
                    continue

                content = docs_transformed[0].page_content
                self.logger.info(f"Content length: {len(content)}")

                # Document splitting
                from langchain_text_splitters import RecursiveCharacterTextSplitter
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1500,
                    chunk_overlap=150,
                    length_function=len,
                )
                chunks = text_splitter.split_text(content)
                self.logger.info(f"Split content into {len(chunks)} chunks.")

                self.logger.info(f'Processing chunks with model {self.llm}')

                for i, chunk in enumerate(chunks):
                    self.logger.info(f"Processing chunk {i+1}/{len(chunks)}...")
                    rich_chunk = f"Source: {label}\n\nContent:\n{chunk}"

                    llm_response = self.llm.run(input_text=rich_chunk)
                    self.neo4j_instance.run(data=llm_response)

                self.logger.info(f'Knowledge graph populated successfully for data source: {label}')
            except Exception as e:
                self.logger.error(f"Error processing {source}: {e}")

    def run(self, input: Union[str, List[float]]) -> str:
        pass
