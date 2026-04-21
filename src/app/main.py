import os
import uvicorn
from dotenv import load_dotenv

# load_dotenv must be before DEFAULT_MODEL_NAME
load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app import utils
from services.Identity_retrival_for_csv import NameIdentityRetrievalForCsv
from services.Identity_retrival_for_html import NameIdentityRetrievalForHtml
from services.cypher_qa import CypherQa

DEFAULT_MODEL_NAME = os.getenv("HF_MODEL_ID", "Qwen/Qwen3-30B-A3B-Instruct-2507")

app = FastAPI(
    title="LLM-WebToGraph",
    description="""This project uses LangChain and Hugging Face-hosted Qwen models to transform data from different sources (web 
    links/csv) to knowledge graph and store then in neo4j DB.""",
    version="0.1.0",
)


@app.get("/query_graph/{question}")
def query_graph(question: str):

    """
    The query_graph function takes a question as input and returns the answer to that question.
    The function uses the CypherQa class to answer graph questions using the configured
    Hugging Face model (HF_MODEL_ID, defaults to Qwen/Qwen3-30B-A3B-Instruct-2507).

    :param question: str: Pass the question to the function
    :return: A htmlresponse object

    """
    try:
        graph_cypher_qachain = CypherQa(model_name=DEFAULT_MODEL_NAME)
        if not graph_cypher_qachain.neo4j_instance.graph:
             return HTMLResponse(content="Neo4j connection is not available. Please check your configuration.", status_code=200)
        response = graph_cypher_qachain.run(question)
        return HTMLResponse(content=response, status_code=200)
    except Exception as e:
        return HTMLResponse(content=f"Error initializing Graph QA: {str(e)}", status_code=200)


from fastapi import FastAPI, BackgroundTasks
# ...

@app.get("/generate_tags_from_html")
async def generate_tags(background_tasks: BackgroundTasks):
    current_dir = os.path.dirname(os.path.abspath(__file__)) # src/app
    src_dir = os.path.dirname(current_dir) # src
    root_dir = os.path.dirname(src_dir) # project root
    
    datasources_path = os.path.join(src_dir, 'datalayer', 'datasources.yml')
    if not os.path.exists(datasources_path):
         datasources_path = os.path.join(root_dir, 'src', 'datalayer', 'datasources.yml')
    
    try:
        ner = NameIdentityRetrievalForHtml(model_name=DEFAULT_MODEL_NAME, data_path=datasources_path)
        if not ner.neo4j_instance.graph:
             return HTMLResponse(content='Neo4j connection not available.', status_code=503)
        
        background_tasks.add_task(ner.run_async)
        return HTMLResponse(content='Successfully started knowledge generation from HTML sources as a background task!!!', status_code=200)
    except Exception as e:
        return HTMLResponse(content=f"Error starting HTML processing: {str(e)}", status_code=500)


@app.get("/generate_tags_from_csv")
def generate_tags(background_tasks: BackgroundTasks):
    current_dir = os.path.dirname(os.path.abspath(__file__)) # src/app
    src_dir = os.path.dirname(current_dir) # src
    root_dir = os.path.dirname(src_dir) # project root

    datasources_path = os.path.join(src_dir, 'datalayer', 'datasources.yml')
    if not os.path.exists(datasources_path):
         datasources_path = os.path.join(root_dir, 'src', 'datalayer', 'datasources.yml')
    
    try:
        ner = NameIdentityRetrievalForCsv(model_name=DEFAULT_MODEL_NAME, data_path=datasources_path)
        if not ner.neo4j_instance.graph:
             return HTMLResponse(content='Neo4j connection not available.', status_code=503)
        
        background_tasks.add_task(ner.run)
        return HTMLResponse(content='Successfully started knowledge generation from CSV sources as a background task!!!', status_code=200)
    except Exception as e:
        return HTMLResponse(content=f"Error starting CSV processing: {str(e)}", status_code=500)


# health check route
@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == '__main__':
    app_config = utils.read_yaml_file('src/app/config.yml')
    load_dotenv(override=True)
    uvicorn.run(app, port=app_config.get('port'), host=app_config.get('host'))
