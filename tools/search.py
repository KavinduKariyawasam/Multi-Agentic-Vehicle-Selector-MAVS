import json
import os
import asyncio
import aiohttp
from urllib.parse import urlparse

from crewai_tools import BaseTool, WebsiteSearchTool


class AsyncSerperSearchTool(BaseTool):
    """
    Asynchronous tool that queries the Serper.dev API for general web search.
    It yields the top few organic results as a newline‑delimited string.
    """

    name = "search_internet"
    description = "Use this tool to perform a general web search for a given query."

    async def run(self, query: str) -> str:
        """
        Perform a Serper search for the supplied query. Returns a formatted string.
        """
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "Serper API key is missing. Please set SERPER_API_KEY."
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": api_key, "content-type": "application/json"}
        payload = json.dumps({"q": query})
        # Run synchronous HTTP in a separate thread to avoid blocking the event loop.
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as resp:
                if resp.status != 200:
                    return f"Serper returned status code {resp.status}"
                data = await resp.json()
        results = data.get("organic", [])
        if not results:
            return "No results found."
        formatted = []
        for result in results[:4]:
            try:
                formatted.append(
                    "\n".join(
                        [
                            f"Title: {result['title']}",
                            f"Link: {result['link']}",
                            f"Snippet: {result['snippet']}",
                            "-----------------",
                        ]
                    )
                )
            except KeyError:
                # Skip entries missing expected keys.
                continue
        return "\n".join(formatted)


class GuardedWebsiteSearchTool(WebsiteSearchTool):
    """
    Extension of WebsiteSearchTool that enforces a strict allowed domain whitelist.
    It filters out any content returned from outside the allowed domains.
    """

    def __init__(self, website: str, allowed_domains: list[str] | None = None, **kwargs):
        super().__init__(website=website, **kwargs)
        self.allowed_domains = allowed_domains or []

    async def run(self, query: str) -> str:
        """
        Perform the website search and post‑filter results by allowed_domains.
        """
        raw_results = await super().run(query)
        if not self.allowed_domains:
            return raw_results
        # naïve filtering: only include lines containing allowed domain names.
        lines = raw_results.splitlines()
        keep = []
        for line in lines:
            if any(allowed in line for allowed in self.allowed_domains):
                keep.append(line)
        return "\n".join(keep)


def create_manufacturer_search_tool(website: str, allowed_domains: list[str] | None = None):
    """
    Factory helper for constructing a domain‑guarded WebsiteSearchTool configured for
    manufacturer sites. Uses a smaller, cheaper model and a lightweight embedder.
    """
    return GuardedWebsiteSearchTool(
        website=website,
        allowed_domains=allowed_domains or [],
        config=dict(
            llm=dict(
                provider="groq",
                config=dict(
                    model="mixtral-8x7b-v2",
                ),
            ),
            embedder=dict(
                provider="huggingface",
                config=dict(
                    model="sentence-transformers/all-MiniLM-L6-v2",
                ),
            ),
        ),
    )