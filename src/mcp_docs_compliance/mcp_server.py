import os

from mcp.server.fastmcp import FastMCP

from .docs_fetch import fetch_visible_text, search_vendor_docs
from .extractor import extract_supported_user_config


mcp = FastMCP("docs-compliance")


@mcp.tool()
async def get_supported_user_config(vendor: str, version: str, topic: str = "username configuration") -> dict:
    """Find vendor docs and extract supported username password/secret syntax."""
    urls = await search_vendor_docs(vendor, version, topic=topic)
    if not urls:
        return {"error": "No documentation URLs found", "vendor": vendor, "version": version}

    combined_text = []
    for url in urls:
        try:
            combined_text.append(await fetch_visible_text(url))
        except Exception:
            continue

    if not combined_text:
        return {"error": "Documentation URLs were found but could not be fetched", "source_urls": urls}

    extracted = extract_supported_user_config("\n".join(combined_text), vendor, version, source_url=urls[0])
    return {**extracted.to_dict(), "source_urls": urls}


if __name__ == "__main__":
    host = os.getenv("MCP_HTTP_HOST", "127.0.0.1")
    port = int(os.getenv("MCP_HTTP_PORT", "8080"))
    mcp.run(transport="http", host=host, port=port)
