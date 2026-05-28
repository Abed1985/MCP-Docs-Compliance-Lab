# MCP Concepts Learned

## What MCP Is

Model Context Protocol is a standard way to expose tools and context to AI clients. Instead of giving an assistant unrestricted access to code, APIs, or shells, you publish explicit tools with typed inputs and outputs.

## Why This Project Uses MCP

The learning goal was to test whether an AI agent could call a tool that understands vendor documentation and returns a structured answer about supported network configuration syntax.

## Tool Boundary

The MCP tool in this repo answers one narrow question:

```text
Given a vendor and software version, what username password/secret syntax appears to be supported?
```

That answer can then be used by a separate compliance checker.

## Transports

MCP can run over different transports:

- `stdio`: useful for local desktop/client integrations.
- HTTP/streamable HTTP: useful for hosted services and remote agents.

## What Was Simplified

The original experiment used Serper, Azure OpenAI, FAISS, LangChain, Playwright, FastAPI, and MCP in one place. The public version separates concerns:

- Regex extraction and compliance are testable offline.
- Web search is optional.
- Azure OpenAI/RAG is documented as a future extension.
- MCP and FastAPI are separate entry points.

## Deployment Notes

- Use Azure Container Apps or App Service for a long-running MCP server.
- Use Azure Functions for stateless helper endpoints.
- Do not commit `.env`, vector indexes, URL caches, or API keys.
