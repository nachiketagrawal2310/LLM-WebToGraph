import os
import uvicorn
from dotenv import load_dotenv
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
    graph_cypher_qachain = CypherQa(model_name=DEFAULT_MODEL_NAME)
    response = graph_cypher_qachain.run(question)
    return HTMLResponse(content=response, status_code=200)


@app.get("/generate_tags_from_html")
async def generate_tags():
    """
    The generate_tags function is a ReST endpoint that will generate the tags for all the data sources.
    This function is called by an external service, such as Jenkins or Travis CI, to ensure that the tags are up-to-date.
    The function returns a 200 status code if successful and 500 otherwise.

    :return: A htmlresponse object with the content as 'successfully generated the knowledge from the data sources!!!' and status_code as 200

    """
    # Resolve absolute path for datasources.yml
    current_dir = os.path.dirname(os.path.abspath(__file__)) # src/app
    src_dir = os.path.dirname(current_dir) # src
    datasources_path = os.path.join(src_dir, 'datalayer', 'datasources.yml')

    ner = NameIdentityRetrievalForHtml(model_name=DEFAULT_MODEL_NAME, data_path=datasources_path)
    ner.run_async()  # asyncronous call since html pages can take time to load and scrape
    return HTMLResponse(content='Successfully generated the knowledge from the data sources!!!', status_code=200)


@app.get("/generate_tags_from_csv")
def generate_tags():
    """
    The generate_tags function is a ReST endpoint that will generate the tags for each of the data sources.
        It uses the NameIdentityRetrievalForCsv class to accomplish this task.
        The model_name and data_path are passed as parameters to this function.

    :return: A htmlresponse object with the status code 200
    """
    # Resolve absolute path for datasources.yml
    current_dir = os.path.dirname(os.path.abspath(__file__)) # src/app
    src_dir = os.path.dirname(current_dir) # src
    datasources_path = os.path.join(src_dir, 'datalayer', 'datasources.yml')
    
    ner = NameIdentityRetrievalForCsv(model_name=DEFAULT_MODEL_NAME, data_path=datasources_path)
    ner.run()
    return HTMLResponse(content='Successfully generated the knowledge from the data sources!!!', status_code=200)


# health check route
@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == '__main__':
    app_config = utils.read_yaml_file('src/app/config.yml')
    load_dotenv()
    uvicorn.run(app, port=app_config.get('port'), host=app_config.get('host'))
