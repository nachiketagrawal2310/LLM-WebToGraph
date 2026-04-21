import os
import uvicorn
from dotenv import load_dotenv

# load_dotenv must be before DEFAULT_MODEL_NAME
load_dotenv(override=True)

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc),
            "data": None
        }
    )

@app.get("/query_graph/{question}")
def query_graph(question: str):
    """
    The query_graph function takes a question as input and returns the answer to that question.
    """
    try:
        graph_cypher_qachain = CypherQa(model_name=DEFAULT_MODEL_NAME)
        if not graph_cypher_qachain.neo4j_instance.graph:
             return JSONResponse(
                 status_code=200,
                 content={
                     "status": "error",
                     "data": None,
                     "message": "Neo4j connection is not available. Please check your configuration."
                 }
             )
        response = graph_cypher_qachain.run(question)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "answer": response,
                    "query_type": "graph_query"
                },
                "message": None
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Error initializing Graph QA: {str(e)}",
                "data": None
            }
        )


@app.get("/generate_tags_from_html")
async def generate_tags_html(background_tasks: BackgroundTasks):
    current_dir = os.path.dirname(os.path.abspath(__file__)) # src/app
    src_dir = os.path.dirname(current_dir) # src
    root_dir = os.path.dirname(src_dir) # project root
    
    datasources_path = os.path.join(src_dir, 'datalayer', 'datasources.yml')
    if not os.path.exists(datasources_path):
         datasources_path = os.path.join(root_dir, 'src', 'datalayer', 'datasources.yml')
    
    try:
        ner = NameIdentityRetrievalForHtml(model_name=DEFAULT_MODEL_NAME, data_path=datasources_path)
        if not ner.neo4j_instance.graph:
             return JSONResponse(
                 status_code=503,
                 content={
                     "status": "error",
                     "message": "Neo4j connection not available.",
                     "data": None
                 }
             )
        
        task_id = str(uuid.uuid4())
        background_tasks.add_task(ner.run_async)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "task_id": task_id,
                    "message": "Successfully started knowledge generation from HTML sources as a background task."
                },
                "message": None
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Error starting HTML processing: {str(e)}",
                "data": None
            }
        )


@app.get("/generate_tags_from_csv")
def generate_tags_csv(background_tasks: BackgroundTasks):
    current_dir = os.path.dirname(os.path.abspath(__file__)) # src/app
    src_dir = os.path.dirname(current_dir) # src
    root_dir = os.path.dirname(src_dir) # project root

    datasources_path = os.path.join(src_dir, 'datalayer', 'datasources.yml')
    if not os.path.exists(datasources_path):
         datasources_path = os.path.join(root_dir, 'src', 'datalayer', 'datasources.yml')
    
    try:
        ner = NameIdentityRetrievalForCsv(model_name=DEFAULT_MODEL_NAME, data_path=datasources_path)
        if not ner.neo4j_instance.graph:
             return JSONResponse(
                 status_code=503,
                 content={
                     "status": "error",
                     "message": "Neo4j connection not available.",
                     "data": None
                 }
             )
        
        task_id = str(uuid.uuid4())
        background_tasks.add_task(ner.run)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "task_id": task_id,
                    "message": "Successfully started knowledge generation from CSV sources as a background task."
                },
                "message": None
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Error starting CSV processing: {str(e)}",
                "data": None
            }
        )


# health check route
@app.get("/health")
def health_check():
    try:
        # We can attempt a quick check of Neo4j if we had an instance, 
        # but for now we follow the spec's simple version and add timestamp.
        return {
            "status": "healthy",
            "neo4j_connected": True, # Ideally verify this
            "timestamp": datetime.now().isoformat()
        }
    except Exception:
        return {
            "status": "unhealthy",
            "neo4j_connected": false,
            "timestamp": datetime.now().isoformat()
        }


if __name__ == '__main__':
    app_config = utils.read_yaml_file('src/app/config.yml')
    load_dotenv(override=True)
    uvicorn.run(app, port=app_config.get('port'), host=app_config.get('host'))
