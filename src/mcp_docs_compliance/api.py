import os

from fastapi import FastAPI
from pydantic import BaseModel

from .compliance import check_user_config_compliance
from .extractor import extract_supported_user_config


app = FastAPI(title="MCP Docs Compliance Lab")


class ExtractRequest(BaseModel):
    vendor: str
    version: str
    documentation_text: str
    source_url: str | None = None


class ComplianceRequest(ExtractRequest):
    actual_config: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract")
def extract(request: ExtractRequest):
    return extract_supported_user_config(
        request.documentation_text,
        request.vendor,
        request.version,
        request.source_url,
    ).to_dict()


@app.post("/check")
def check(request: ComplianceRequest):
    supported = extract_supported_user_config(
        request.documentation_text,
        request.vendor,
        request.version,
        request.source_url,
    )
    return check_user_config_compliance(request.actual_config, supported)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "mcp_docs_compliance.api:app",
        host=os.getenv("FASTAPI_HOST", "127.0.0.1"),
        port=int(os.getenv("FASTAPI_PORT", "8001")),
        reload=True,
    )
