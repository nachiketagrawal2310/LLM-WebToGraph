import os
import json
import re
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app import utils
from components.base_component import BaseComponent

load_dotenv(override=True)


DEFAULT_HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"


def build_hf_chat_model(model: str = None, max_tokens: int = 2048):
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
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=0.01,
        repetition_penalty=1.03,
        huggingfacehub_api_token=api_token,
    )
    return ChatHuggingFace(llm=endpoint)


def get_schema():
    """
    The get_schema function reads the schema.yml file and returns a dictionary of the schema.

    :return: The schema
    """
    schema_path = os.path.join(os.getcwd(), 'src/services/schema.yml')
    if not os.path.exists(schema_path):
         # Try alternative if running from src
         schema_path = os.path.join(os.getcwd(), 'services/schema.yml')
    
    schema = utils.read_yaml_file(schema_path)
    return schema


class Llm(BaseComponent):

    def __init__(self, model: str, max_tokens: int = 4096):
        super().__init__('Llm')
        self.model = model or os.getenv("HF_MODEL_ID", DEFAULT_HF_MODEL)
        self.llm = build_hf_chat_model(self.model, max_tokens=max_tokens)

    @staticmethod
    def _clean_json_text(raw_text: str) -> str:
        """Extract the JSON block from markdown code fences or the whole text."""
        # Find JSON block in markdown
        match = re.search(r"```(?:json)?\s*(\{.*\}|\[.*\])\s*```", raw_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # If no fences, try to find any { ... } or [ ... ] block
        match = re.search(r"(\{.*\}|\[.*\])", raw_text, re.DOTALL)
        if match:
             return match.group(1).strip()
             
        return raw_text.strip()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def _invoke_with_retry(self, prompt):
        """Invoke LLM with retry logic for 503s/timeouts."""
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            self.logger.warning(f"LLM invocation failed, retrying... Error: {e}")
            raise

    def _invoke_json_fallback(self, input_text, schema_name="KnowledgeGraph"):
        if schema_name == "KnowledgeGraph":
            prompt = (
                "Task: Extract a detailed knowledge graph from the given input.\n"
                "CRITICAL Rules for structuring:\n"
                "1. Identify all primary entities (nodes) and their relationships (rels).\n"
                "2. Standardize Entity IDs (e.g., capitalize appropriately, remove extra spacing) so that references to the same entity merge into one node.\n"
                "3. If the text identifies a 'Source URL:', you MUST create a central node with type 'WebResource' using the URL as its 'id'. Link all other extracted main entities to this WebResource node using an 'EXTRACTED_FROM' relationship.\n"
                "4. If no URL is present, infer a central node representing the dataset (e.g., 'Movies Dataset', 'Scientific Topic') and link the entities to it using 'PART_OF'.\n"
                "5. Only use descriptive string values for relationships 'type'.\n"
                "6. Ensure the 'id' field for each node is unique and descriptive.\n"
                "7. Return ONLY valid JSON containing exactly the 'nodes' and 'rels' keys, with NO extra markdown or conversational text.\n\n"
                "Example Formats for structured relations:\n"
                "Input: 'A movie named Inception (1999)'\n"
                "{\n"
                '  "nodes": [\n'
                '    {"id": "Dataset_Movies", "type": "Dataset", "properties": {"description": "A collection of movies"}},\n'
                '    {"id": "Inception", "type": "Movie", "properties": {"year": "1999"}}\n'
                '  ],\n'
                '  "rels": [\n'
                '    {"source": "Inception", "target": "Dataset_Movies", "type": "PART_OF", "properties": {}}\n'
                '  ]\n'
                "}\n\n"
                f"Input:\n{input_text}"
            )
        else:
            prompt = (
                "Extract information and return ONLY valid JSON matching this schema. "
                "Do not include markdown.\n\n"
                f"Input:\n{input_text}"
            )
            
        response = self._invoke_with_retry(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        cleaned = self._clean_json_text(content)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM JSON: {e}")
            self.logger.error(f"Raw content: {content}")
            self.logger.error(f"Cleaned content: {cleaned}")
            return {"nodes": [], "rels": []}

    def _format_to_kg_schema(self, raw_data):
        """Helper to convert loose LLM JSON into strict KnowledgeGraph schema."""
        if not isinstance(raw_data, dict): return raw_data
        
        nodes = raw_data.get('nodes', [])
        rels = raw_data.get('rels', [])
        
        formatted_nodes = []
        node_map = {}
        for node in nodes:
            if not isinstance(node, dict): continue
            node_id = str(node.get('id', ''))
            node_type = node.get('type', 'Entity')
            props = node.get('properties', {})
            
            # Keep dict properties as is
            if not isinstance(props, dict):
                 props = {}
                
            fn = {'id': node_id, 'type': node_type, 'properties': props}
            formatted_nodes.append(fn)
            node_map[node_id] = fn
            
        formatted_rels = []
        for rel in rels:
            if not isinstance(rel, dict): continue
            source_raw = rel.get('source', '')
            target_raw = rel.get('target', '')
            rel_type = rel.get('type', 'RELATED_TO')
            props = rel.get('properties', {})
            if not isinstance(props, dict): props = {}
            
            # Resolve source/target from IDs if they are just strings/ints
            if isinstance(source_raw, (str, int)):
                source = node_map.get(str(source_raw), {'id': str(source_raw), 'type': 'Entity', 'properties': {}})
            else:
                source = source_raw
                
            if isinstance(target_raw, (str, int)):
                target = node_map.get(str(target_raw), {'id': str(target_raw), 'type': 'Entity', 'properties': {}})
            else:
                target = target_raw
            
            formatted_rels.append({
                'source': source,
                'target': target,
                'type': rel_type,
                'properties': props
            })
            
        return {'nodes': formatted_nodes, 'rels': formatted_rels}

    def run(self, input_text, schema=None):
        """
        Processes input text and returns structured data.
        """
        from datalayer.KnowledgeGraph import KnowledgeGraph
        
        target_schema = schema or KnowledgeGraph
        self.logger.info(f"Extracting with schema: {target_schema}")

        try:
            self.logger.info("Trying structured output...")
            chain = self.llm.with_structured_output(target_schema)
            llm_response = chain.invoke(input_text)
            self.logger.info(f"Structured output success")
        except Exception as ex:
            self.logger.warning(f"Structured output failed, using JSON fallback: {ex}")
            llm_response_dict = self._invoke_json_fallback(input_text=input_text)
            
            # Format the loose dict into strict schema format
            formatted_dict = self._format_to_kg_schema(llm_response_dict)
            
            if target_schema == KnowledgeGraph:
                try:
                    llm_response = KnowledgeGraph(**formatted_dict)
                except Exception as pydantic_ex:
                    self.logger.error(f"Pydantic validation failed even after formatting: {pydantic_ex}")
                    # Fallback to a minimal or partial response
                    llm_response = KnowledgeGraph(nodes=[], rels=[])
            else:
                llm_response = llm_response_dict

        return llm_response
