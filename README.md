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

5. **Svelte:** A modern, reactive frontend for querying and visualizing the knowledge graph.

## Features

- Web scraping from various sources, such as web links and CSV files.
- Data transformation and extraction using **Hugging Face-hosted Qwen models**.
- Population of a structured knowledge graph in Neo4j Aura Database.
- FastAPI-based health check API to monitor the application's status.
- **Svelte SPA** for a responsive user experience.
- Legacy Streamlit web application for backwards compatibility.

## Project Layout

```text
LLM-WebToGraph/
├── src/
│   ├── app/           # Core LLM app logic and FastAPI entrypoint
│   ├── components/    # Shared base components
│   ├── datalayer/     # Neo4j dumpers, graph models, preprocessing
│   ├── services/      # CSV/HTML ingestion and Cypher QA services
│   ├── data/          # Sample/source datasets
│   └── UI/            # Legacy Streamlit UI
├── src/
│   └── frontend/      # New Svelte SPA Frontend
├── scripts/
│   ├── debug/         # Debug and troubleshooting scripts
│   ├── diagnostics/   # Environment and dependency diagnostics
│   └── verify/        # External connectivity checks (HF/Neo4j)
├── tests/
│   └── smoke/         # Lightweight import and capability smoke checks
├── requirements.txt
├── run.sh             # Unified script to start both Backend and Svelte Frontend
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js (v18+) and npm
- Neo4j Database (AuraDB or Local)
- Hugging Face API Token

### Installation & Run

1. **Clone and Configure**
   - Ensure data files are in `src/data/` if using CSVs.
   - Update `src/datalayer/datasources.yml` with any HTML links.

2. **Setup Backend**
   ```bash
   # Create and activate virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   cd src/frontend
   npm install
   cd ../
   ```

4. **Configure Credentials**
   - Update `src/app/config.yml` with your Neo4j URI and credentials.
   - Set your Hugging Face token in environment variables (`HUGGINGFACEHUB_API_TOKEN` or `HF_TOKEN`).

5. **Run the Application (Recommended)**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
   *This starts both the FastAPI backend (port 8000) and Svelte frontend (port 5173).*

   **Manual Start:**

   *Backend:*
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/src
   python3 src/app/main.py
   ```

   *Frontend (Svelte):*
   ```bash
   cd src/frontend
   npm run dev
   ```

   *Legacy Frontend (Streamlit):*
   ```bash
   streamlit run src/UI/ui.py
   ```

### Utility Scripts

```bash
# Diagnostics
python scripts/diagnostics/check_capabilities.py
python scripts/diagnostics/list_models.py

# Verification
python scripts/verify/verify_hf_connection.py
python scripts/verify/verify_neo4j.py

# Debug helpers
python scripts/debug/debug_ingestion.py
python scripts/debug/debug_qa.py
```
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
