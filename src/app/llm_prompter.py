import os
from typing import List, Optional

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document

from app import utils
from app.llm import DEFAULT_HF_MODEL, build_hf_chat_model
from components.base_component import BaseComponent
from datalayer.KnowledgeGraph import KnowledgeGraph

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


class LlmPrompter(BaseComponent):

    def __init__(self, model: str):
        super().__init__('LlmPrompter')

        self.model = model or os.getenv("HF_MODEL_ID", DEFAULT_HF_MODEL)
        self.llm = build_hf_chat_model(self.model)

    def run(self, document: Document,
            nodes: Optional[List[str]] = None,
            rels: Optional[List[str]] = None):
        return self.extract_and_store_graph(document, nodes, rels)

    def get_extraction_chain(self,
                             allowed_nodes: Optional[List[str]] = None,
                             allowed_rels: Optional[List[str]] = None
                             ):
        prompt = ChatPromptTemplate.from_messages(
            [(
                "system",
                f"""# Knowledge Graph Instructions
    ## 1. Overview
    You are a top-tier algorithm designed for extracting information in structured formats to build a knowledge graph.
    - **Nodes** represent entities and concepts. They're akin to largest infrastructure projects nodes.
    - The aim is to achieve simplicity and clarity in the knowledge graph, making it accessible for a vast audience.
    ## 2. Labeling Nodes
    - **Consistency**: Ensure you use basic or elementary types for node labels.
      - For example, when you identify an entity representing a person, always label it as **"person"**. Avoid using more specific terms like "mathematician" or "scientist".
    - **Node IDs**: Never utilize integers as node IDs. Node IDs should be names or human-readable identifiers found in the text.
    {'- **Allowed Node Labels:**' + ", ".join(allowed_nodes) if allowed_nodes else ""}
    {'- **Allowed Relationship Types**:' + ", ".join(allowed_rels) if allowed_rels else ""}
    ## 3. Handling Numerical Data and Dates
    - Numerical data, like age or other related information, should be incorporated as attributes or properties of the respective nodes.
    - **No Separate Nodes for Dates/Numbers**: Do not create separate nodes for dates or numerical values. Always attach them as attributes or properties of nodes.
    - **Property Format**: Properties must be in a key-value format.
    - **Quotation Marks**: Never use escaped single or double quotes within property values.
    ## 4. Coreference Resolution
    - **Maintain Entity Consistency**: When extracting entities, it's vital to ensure consistency.
    If an entity, such as "John Doe", is mentioned multiple times in the text but is referred to by different names or pronouns (e.g., "Joe", "he"),
    always use the most complete identifier for that entity throughout the knowledge graph. In this example, use "John Doe" as the entity ID.
    Remember, the knowledge graph should be coherent and easily understandable, so maintaining consistency in entity references is crucial.
    ## 5. Strict Compliance
    Adhere to the rules strictly. Non-compliance will result in termination.
              """),
                ("human", "Use the given format to extract information from the following input: {input}"),
                ("human", "Tip: Make sure to answer in the correct format"),
            ])
        # Use with_structured_output with Pydantic model
        return prompt | self.llm.with_structured_output(KnowledgeGraph)

    def extract_and_store_graph(self,
                                document: Document,
                                nodes: Optional[List[str]] = None,
                                rels: Optional[List[str]] = None):
        # Extract graph data using structured output
        extract_chain = self.get_extraction_chain(nodes, rels)
        # Run the chain (prompt | model)
        data = extract_chain.invoke({"input": document.page_content})
        return data
