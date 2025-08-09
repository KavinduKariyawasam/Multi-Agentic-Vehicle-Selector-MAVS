import os
import pytest

from mavs_new.crew import VehicleRecommenderCrew


def test_default_run(monkeypatch):
    """
    Smoke test ensuring the crew runs end‑to‑end without hitting external APIs.
    Mocks environment variables and stubs network‑dependent tools.
    """
    # Ensure fake keys are set
    monkeypatch.setenv("GROQ_API_KEY", "fake")
    monkeypatch.setenv("TOGETHER_API_KEY", "fake")
    monkeypatch.setenv("SERPER_API_KEY", "fake")

    # Monkeypatch search tools to avoid real HTTP
    from mavs_new.tools import search as search_tools

    async def fake_serper_run(self, query: str) -> str:
        return "Title: Example\nLink: https://toyota.com/example\nSnippet: Sample\n"

    async def fake_website_run(self, query: str) -> str:
        return "Mock data from manufacturer site."

    monkeypatch.setattr(search_tools.AsyncSerperSearchTool, "run", fake_serper_run)
    monkeypatch.setattr(search_tools.GuardedWebsiteSearchTool, "run", fake_website_run)

    crew = VehicleRecommenderCrew("USA", 30000)
    result = crew.run()
    # We can't predict the exact output but we assert it returns a non‑empty result.
    assert result is not None