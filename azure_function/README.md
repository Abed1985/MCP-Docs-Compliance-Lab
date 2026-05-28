# Azure Function Option

This folder shows the part of the project that is worth deploying as an Azure Function: a stateless HTTP compliance check.

The MCP server itself is a long-running tool server, so Azure Container Apps, App Service, or a VM/container runtime is a better fit for the MCP transport. Azure Functions are still useful for stateless helper APIs such as `/check-compliance`.

## Deploy Sketch

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt azure-functions
func init --python
func start
```

For a real deployment, configure app settings instead of committing `.env` files.
