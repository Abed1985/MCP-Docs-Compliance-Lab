# MCP Docs Compliance Lab

A public-safe learning project that demonstrates how a Model Context Protocol server can expose documentation-aware tools to AI agents.

The original private experiment mixed FastAPI, FastApiMCP, Serper search, Azure OpenAI, FAISS, LangChain, Playwright loading, and a small web UI. This repo keeps the learning story but simplifies the implementation so it is easier to revisit, test, and explain.

## Portfolio Story

This project shows that I can:

- Build a small MCP tool server.
- Wrap the same core logic in a FastAPI endpoint.
- Parse vendor documentation into structured data.
- Compare supported syntax with actual network device configuration.
- Keep API keys, vector indexes, caches, and generated files out of Git.
- Explain when Azure Functions make sense and when a container/App Service is a better MCP host.

## What It Does

The core workflow is:

```text
AI client or API caller
        |
        v
MCP tool / FastAPI endpoint
        |
        v
Vendor documentation text or optional web search
        |
        v
Username password/secret syntax extraction
        |
        v
Compliance comparison against actual config
```

Example supported syntax extracted from docs:

```text
username admin password 5 <hashed-password>
username admin secret 9 <hashed-secret>
```

Example actual config:

```text
username netops secret 9 $9$example
```

The compliance checker returns whether the actual password/secret type matches what documentation says is supported.

## Repository Layout

```text
.
|-- azure_function/              # Optional stateless Azure Functions example
|-- docs/
|   |-- concepts.md              # MCP learning notes
|   `-- index.html               # Static GitHub Pages concept page
|-- src/mcp_docs_compliance/
|   |-- api.py                   # FastAPI wrapper
|   |-- compliance.py            # Config compliance checker
|   |-- docs_fetch.py            # Optional Serper/docs fetch helper
|   |-- extractor.py             # Documentation syntax extractor
|   |-- mcp_server.py            # MCP tool server
|   |-- models.py
|   `-- __init__.py
|-- tests/
|-- .env.example
|-- README.md
|-- pyproject.toml
`-- requirements.txt
```

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
PYTHONPATH=src pytest
```

Run the FastAPI wrapper:

```bash
PYTHONPATH=src python -m mcp_docs_compliance.api
```

Run the MCP server:

```bash
PYTHONPATH=src python -m mcp_docs_compliance.mcp_server
```

## FastAPI Example

```bash
curl -X POST http://127.0.0.1:8001/check \
  -H 'Content-Type: application/json' \
  -d '{
    "vendor": "cisco",
    "version": "IOS-XE 17",
    "documentation_text": "username admin password 5 <hash>\nusername admin secret 9 <hash>",
    "actual_config": "username netops secret 9 $9$example"
  }'
```

## MCP Tool

The MCP server exposes:

```text
get_supported_user_config(vendor: str, version: str, topic: str = "username configuration") -> dict
```

It optionally uses Serper to find vendor docs and then extracts username password/secret syntax from visible page text.

## GitHub Pages

The `docs/index.html` file is a static concept page that can be enabled with GitHub Pages. It does not call the backend; it explains the project and MCP flow publicly.

## Azure Deployment Notes

See `azure_function/README.md`.

Short version:

- Azure Functions are useful for stateless HTTP helpers like `/check-compliance`.
- A long-running MCP server is usually better suited to Azure Container Apps, App Service, or another always-on container/runtime.

## Sanitization Notes

The original folder contained live-looking `.env` values and generated state. This public repo excludes:

- `SERPER_API_KEY`, `SERP_API_KEY`, Azure OpenAI keys, and Azure endpoints.
- FAISS indexes and pickle files.
- URL caches such as `seen_urls.json` and `embedded_docs_cache.json`.
- Virtual environments.
- Experimental `.bak` files.
- Local IP-bound server settings.

Use `.env.example` as the only public configuration reference.

## Learning Notes

See `docs/concepts.md` for the main MCP concepts captured while building this lab.
