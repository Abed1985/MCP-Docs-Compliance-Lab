import json
import os
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


SERPER_URL = "https://google.serper.dev/search"
DOC_DOMAINS = {
    "cisco": "cisco.com/c/en/us/td/docs",
    "juniper": "juniper.net/documentation",
    "fortinet": "docs.fortinet.com",
}


def docs_domain_for(vendor):
    return DOC_DOMAINS.get(vendor.lower(), f"{vendor.lower()}.com")


async def search_vendor_docs(vendor, version, topic="username configuration", limit=3):
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise RuntimeError("SERPER_API_KEY is not set. Use static text extraction or configure .env.")

    query = f"{version} {topic} site:{docs_domain_for(vendor)}"
    payload = {"q": query, "num": limit}
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(SERPER_URL, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        results = response.json().get("organic", [])
        return [item["link"] for item in results[:limit] if "link" in item]


async def fetch_visible_text(url):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http/https URLs are supported")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, timeout=30)
        response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()
    return soup.get_text("\n", strip=True)
