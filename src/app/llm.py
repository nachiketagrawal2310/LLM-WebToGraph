import os
import backoff
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

from app import utils
from components.base_component import BaseComponent

load_dotenv()


def get_schema():
    """
    The get_schema function reads the schema.yml file and returns a dictionary of the schema.

    :return: The schema
    :doc-author: Trelent
    """
    schema_path = os.path.join(os.getcwd(), 'src/services/schema.yml')
    if not os.path.exists(schema_path):
         # Try alternative if running from src
         schema_path = os.path.join(os.getcwd(), 'services/schema.yml')
    
    schema = utils.read_yaml_file(schema_path)
    return schema


class Llm(BaseComponent):

    def __init__(self, model: str):
        super().__init__('Llm')
        self.model = model or "gemini-2.5-flash"
        self.llm = ChatGoogleGenerativeAI(temperature=0, model=self.model, google_api_key='AIzaSyBt8hNgFnkNlm5UHy3pHdPjMPyI44ZLbTw')

    def run(self, input_text):
        """
        The run function is the main entry point for your component.
        It will be called with a string of text to process, and should return a dictionary of results.
        The keys in this dictionary are the names of slots that you defined in your schema.

        :param self: Represent the instance of the class
        :param input_text: Pass the text that we want to extract entities from
        :return: A dictionary with the following structure:
        """
        schema = get_schema()
        self.logger.info(f'schema: {schema}')
        
        # Use with_structured_output which is the modern way and works with Gemini
        # We pass the schema (dict) directly.
        chain = self.llm.with_structured_output(schema)
        # Runnable uses invoke, not run.
        llm_response = chain.invoke(input_text)
        self.logger.info(f'llm_response: {llm_response}')
        return llm_response
