import os
import json
import re
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from app import utils
from components.base_component import BaseComponent

load_dotenv()


DEFAULT_HF_MODEL = "Qwen/Qwen3-30B-A3B-Instruct-2507"


def build_hf_chat_model(model: str = None):
    """Build a Hugging Face chat model using the serverless inference endpoint."""
    repo_id = model or os.getenv("HF_MODEL_ID", DEFAULT_HF_MODEL)
    api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN")
    if not api_token:
        raise ValueError(
            "Missing Hugging Face token. Set HUGGINGFACEHUB_API_TOKEN or HF_TOKEN."
        )

    provider = os.getenv("HF_INFERENCE_PROVIDER", "auto")
    endpoint = HuggingFaceEndpoint(
        repo_id=repo_id,
        task="text-generation",
        provider=provider,
        max_new_tokens=2048,
        do_sample=False,
        repetition_penalty=1.03,
        huggingfacehub_api_token=api_token,
    )
    return ChatHuggingFace(llm=endpoint)


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
        self.model = model or os.getenv("HF_MODEL_ID", DEFAULT_HF_MODEL)
        self.llm = build_hf_chat_model(self.model)

    @staticmethod
    def _clean_json_text(raw_text: str) -> str:
        """Remove markdown fences and keep the JSON object payload."""
        text = raw_text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\\s*", "", text)
            text = re.sub(r"\\s*```$", "", text)
        return text.strip()

    def _invoke_json_fallback(self, input_text, schema):
        schema_text = json.dumps(schema, ensure_ascii=True, indent=2)
        prompt = (
            "Extract the information from the input and return ONLY valid JSON "
            "that conforms to this schema. Do not include markdown or extra keys.\\n\\n"
            f"Schema:\\n{schema_text}\\n\\n"
            f"Input:\\n{input_text}"
        )
        response = self.llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        cleaned = self._clean_json_text(content)
        return json.loads(cleaned)

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

        try:
            chain = self.llm.with_structured_output(schema)
            llm_response = chain.invoke(input_text)
        except Exception as ex:
            self.logger.warning(f"Structured output failed, using JSON fallback: {ex}")
            llm_response = self._invoke_json_fallback(input_text=input_text, schema=schema)

        self.logger.info(f'llm_response: {llm_response}')
        return llm_response
