# LLM-WebToGraph

LLM-WebToGraph is a powerful project that harnesses the capabilities of LangChain and Hugging Face-hosted language models (LLMs) to scrape data from various sources on the web, transforming it into a structured knowledge graph. This knowledge graph is then populated into a Neo4j Aura Database, providing an efficient way to store, query, and retrieve information using Cypher queries and LLMs. With the synergy of LangChain, Hugging Face models, and Neo4j, this project offers a robust solution for knowledge management and retrieval.

## Architecture
![design](https://github.com/prvnsingh/LLM-WebToGraph/blob/main/design.jpeg?raw=true)


## Overview

The LLM-WebToGraph project combines several key components to achieve its goal:

1. **Langchain:** A language model designed for natural language understanding and generation, powering the core of the project.

2. **Hugging Face-hosted Language Models (LLMs):** These models are used to extract and process data from various sources, converting unstructured data into structured knowledge.

3. **Neo4j Aura Database:** The project stores the structured knowledge graph in a Neo4j Aura Database, allowing for efficient storage and retrieval.

4. **FastAPI:** To expose an API for interacting with the project and to check its health status.

5. **Streamlit:** For building a user-friendly interface to query and visualize the knowledge graph.

## Features

- Web scraping from various sources, such as web links and CSV files.
- Data transformation and extraction using **Hugging Face-hosted Qwen models**.
- Population of a structured knowledge graph in Neo4j Aura Database.
- FastAPI-based health check API to monitor the application's status.
- Streamlit web application for querying and visualizing the knowledge graph.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Neo4j Database (AuraDB or Local)
- Hugging Face API Token

### Installation & Run

1. **Clone and Configure**
   - Ensure data files are in `src/data/` if using CSVs.
   - Update `src/datalayer/datasources.yml` with any HTML links.

2. **Setup Environment**
   ```bash
   # Create and activate virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure Credentials**
   - Update `src/app/config.yml` with your Neo4j URI and credentials.
   - Set your Hugging Face token in environment variables (`HUGGINGFACEHUB_API_TOKEN` or `HF_TOKEN`).

4. **Run the Application**

   **Backend (FastAPI):**
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/src
   python src/app/main.py
   ```
   *Access Swagger documentation at: http://localhost:8000/docs*

   **Frontend (Streamlit):**
   ```bash
   streamlit run src/UI/ui.py
   ```
   *Access UI at: http://localhost:8501/*
## Working directory
![Directory Tree](https://github.com/prvnsingh/LLM-WebToGraph/blob/main/dirTree.jpg?raw=true)

## Demo snapshot
![Demo snapshot](https://github.com/prvnsingh/LLM-WebToGraph/blob/main/working.jpg?raw=true)

## Contributing

Contributions to the LLM-WebToGraph project are welcome! If you'd like to contribute, please follow these guidelines:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and ensure tests pass.
- Submit a pull request.

## Future Scope
In the future, the project can be extended with a microservices architecture, including:

A separate data service responsible for ingesting data from S3.
Utilization of a Selenium bot to scrape the web and download CSV files.
Integration with more data sources for enhanced knowledge graph creation.

## References
- [Langchain Graph Transformer Documentation](https://python.langchain.com/docs/use_cases/graph/diffbot_graphtransformer)
- [Langchain Cypher Query Documentation](https://python.langchain.com/docs/use_cases/graph/graph_cypher_qa)
- [Blog Post: Constructing Knowledge Graphs from Text](https://blog.langchain.dev/constructing-knowledge-graphs-from-text/)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
# LLM-WebToGraph
