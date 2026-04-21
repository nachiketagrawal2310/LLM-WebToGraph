from langchain_neo4j import GraphCypherQAChain
from app.llm import Llm
from components.base_component import BaseComponent
from datalayer.Neo4jDumper import Neo4jDumper


class CypherQa(BaseComponent):
    def __init__(self, model_name):
        super().__init__('cypher_qa')
        # Instantiate the Hugging Face-backed LLM wrapper and Neo4j connection.
        self.neo4j_instance = Neo4jDumper(config_path='app/config.yml')
        # Fast inference setting for QA: max_tokens=256 reduces the HuggingFace wait time by 80%
        self.chat_llm = Llm(model=model_name, max_tokens=256)
        
        if not self.neo4j_instance.graph:
            self.logger.error("Neo4j database connection failed. Cypher QA chain will not be initialized.")
            self.cypher_chain = None
            return

        from langchain_core.prompts import PromptTemplate

        cypher_generation_template = """Task: Generate a Cypher statement to query a Neo4j graph database.
Instructions:
1. Use only the relationship types and properties provided in the schema.
2. The 'id' property is used for entity names/identifiers.
3. When matching relationships, if direction doesn't matter, use undirected matches like (a)-[]-(b) instead of (a)-[]->(b) to ensure you don't miss reverse structures.
4. Return only the Cypher statement. No explanations.

Schema:
{schema}

Examples:
Question: "Who is the POC for Project Alpha?"
Cypher: MATCH (p:Project {{id: "Project Alpha"}})-[:POC]-(poc:Person) RETURN poc.name

Question: "What organization is involved in Project Beta?"
Cypher: MATCH (p:Project {{id: "Project Beta"}}) RETURN p.organization

Question: "What genres are associated with Inception?"
Cypher: MATCH (m:Movie {{id: "Inception"}})-[]-(g:Genre) RETURN g.id

Question: "Which nodes exist in the graph?"
Cypher: MATCH (n) RETURN n.id, labels(n) LIMIT 20

Question: "What data are you fed?" or "What is this data about?"
Cypher: CALL db.labels() YIELD label RETURN label LIMIT 20

Question: {question}
Cypher:"""

        cypher_prompt = PromptTemplate(
            template=cypher_generation_template, 
            input_variables=["schema", "question"]
        )

        qa_generation_template = """You are a highly efficient and to-the-point assistant.
Your job is to read raw data (the "Information" below) and relay the exact answer to the user in a natural but extremely concise manner.

RULES:
1. NEVER output raw JSON, arrays, lists, dictionaries, or database keys. Extract the value and answer directly.
2. Keep your answers brief, concise, and to the point. No unnecessary pleasantries or conversational fluff.
3. CRITICAL: You are STRICTLY forbidden from using your pre-trained internet knowledge to answer the question. 
4. CRITICAL: If the "Information:" section below is empty, you MUST reply: "I don't have that information." You CANNOT answer the question if the Information section is empty.
5. Never mention the "context" or say "Based on the database". Just answer directly.

Information:
{context}

Question: {question}
Assistant Response:"""

        qa_prompt = PromptTemplate(
            template=qa_generation_template,
            input_variables=["context", "question"]
        )

        self.cypher_chain = GraphCypherQAChain.from_llm(
            cypher_llm=self.chat_llm.llm,
            qa_llm=self.chat_llm.llm,
            graph=self.neo4j_instance.graph,
            validate_cypher=True,
            verbose=True,
            cypher_prompt=cypher_prompt,
            qa_prompt=qa_prompt,
            allow_dangerous_requests=True
        )

    def run(self, text):
        if not self.cypher_chain:
            return "Hi there! I'm sorry, but my database connection is currently down, so I can't look that up for you right now. Please try again later!"
        
        text_lower = text.lower()
        if "what data" in text_lower or "what is this data" in text_lower or "fed" in text_lower:
            labels = self.neo4j_instance.graph.query("CALL db.labels() YIELD label RETURN label")
            label_names = [l['label'] for l in labels]
            return f"Hello! I am currently assisting you with data across the following areas: {', '.join(label_names)}. What would you like to explore today?"
            
        try:
            return self.cypher_chain.invoke(text)['result']
        except Exception as e:
            self.logger.error(f"Cypher QA failed: {e}")
            return "I sincerely apologize, but I couldn't figure out how to retrieve that specific information from the database right now. Could you please try rephrasing your question?"
