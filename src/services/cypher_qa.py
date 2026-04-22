from langchain_neo4j import GraphCypherQAChain
from app.llm import Llm
from components.base_component import BaseComponent
from datalayer.Neo4jDumper import Neo4jDumper
from duckduckgo_search import DDGS


class CypherQa(BaseComponent):
    def __init__(self, model_name):
        super().__init__('cypher_qa')
        # Instantiate the Hugging Face-backed LLM wrapper and Neo4j connection.
        self.neo4j_instance = Neo4jDumper(config_path='app/config.yml')
        # Fast inference setting for QA: max_tokens=512 for more detailed internet fallback
        self.chat_llm = Llm(model=model_name, max_tokens=512)
        
        if not self.neo4j_instance.graph:
            self.logger.error("Neo4j database connection failed. Cypher QA chain will not be initialized.")
            self.cypher_chain = None
            return

        from langchain_core.prompts import PromptTemplate

        # Improved Cypher prompt with case-insensitive and partial matching logic
        cypher_generation_template = """Task: Generate a Cypher statement to query a Neo4j graph database.
Instructions:
1. Use only the relationship types and properties provided in the schema.
2. The 'id' property is used for entity names/identifiers.
3. CRITICAL: Use `CONTAINS` and `toLower()` for fuzzy string matching to avoid exact match failures.
4. For example, instead of `{{id: "Apple"}}`, use `WHERE toLower(n.id) CONTAINS "apple"`.
5. Return only the Cypher statement. No explanations.

Schema:
{schema}

Examples:
Question: "Who is the CEO of Apple?"
Cypher: MATCH (c:Company) WHERE toLower(c.id) CONTAINS "apple" RETURN c.CurrentCEO

Question: "Papers on climate?"
Cypher: MATCH (p:Paper) WHERE toLower(p.Title) CONTAINS "climate" OR toLower(p.Abstract) CONTAINS "climate" RETURN p.Title

Question: {question}
Cypher:"""

        cypher_prompt = PromptTemplate(
            template=cypher_generation_template, 
            input_variables=["schema", "question"]
        )

        # Relaxed QA prompt that allows for fallback
        qa_generation_template = """You are an expert research assistant.
Answer the question based on the "Information" provided. 

Rules:
1. If the "Information" is helpful, use it to give a precise, grounded answer.
2. If the "Information" is empty or not helpful, but you have relevant knowledge (from your training or provided search context), answer the question directly.
3. Be professional, academic, and concise.

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

    def _web_search(self, query: str) -> str:
        """Fallback to DuckDuckGo search if the graph has no answer."""
        try:
            self.logger.info(f"Attempting web search fallback for: {query}")
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if results:
                    search_context = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
                    return f"\n(Search Results Fallback):\n{search_context}"
        except Exception as e:
            self.logger.error(f"Web search failed: {e}")
        return ""

    def run(self, text):
        if not self.cypher_chain:
            return "Database connection is down. Please check your Neo4j configuration."
        
        text_lower = text.lower()
        if "what data" in text_lower or "what is this data" in text_lower or "fed" in text_lower:
            try:
                labels = self.neo4j_instance.graph.query("CALL db.labels() YIELD label RETURN label")
                label_names = [l['label'] for l in labels]
                return f"I am currently assisting you with data across the following areas: {', '.join(label_names)}."
            except:
                return "The knowledge graph is currently empty or unreachable."
            
        try:
            # 1. Try Graph Search
            result_obj = self.cypher_chain.invoke(text)
            answer = result_obj['result']
            
            # 2. If Graph says it doesn't know, try Web Search Fallback
            if "i don't have that information" in answer.lower() or "not found" in answer.lower() or "not in the database" in answer.lower():
                search_data = self._web_search(text)
                if search_data:
                    # Re-invoke LLM with search context
                    prompt = f"Question: {text}\n\nInformation from Web Search:\n{search_data}\n\nPlease answer based on the search results."
                    fallback_response = self.chat_llm.llm.invoke(prompt)
                    return fallback_response.content if hasattr(fallback_response, "content") else str(fallback_response)
            
            return answer
        except Exception as e:
            self.logger.error(f"QA execution failed: {e}")
            # Final fallback: just let the LLM answer if it can
            try:
                 search_data = self._web_search(text)
                 prompt = f"User Question: {text}\n\nSearch Context:\n{search_data}\n\nExpert Answer:"
                 response = self.chat_llm.llm.invoke(prompt)
                 return response.content if hasattr(response, "content") else str(response)
            except:
                 return "I encountered an error while processing your request. Please try again later."
