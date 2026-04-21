# Scripts

Operational helper scripts are grouped by intent:

- `debug/`: Focused debugging scripts for ingestion and QA flows.
- `diagnostics/`: Environment capability checks and model discovery helpers.
- `verify/`: Connectivity checks for external dependencies (Hugging Face, Neo4j).

All scripts are written to resolve the project root and `src/` dynamically, so they can be run from any working directory.
