import os
from textwrap import dedent

from crewai import Agent
from crewai.tools import PythonREPL
from langchain_groq import ChatGroq            # pip install langchain-groq


class CustomAgents:
    """Factory for the two agents used in this project."""

    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set.  Put it in your shell or a .env file."
            )

        # One shared LLM instance keeps token-usage predictable
        self.llm = ChatGroq(
            model_name="llama3-8b-8192",
            api_key=api_key,
            temperature=0.7,
        )

    # --------------------------------------------------------------------- #
    # 1) Agent that SCRAPES manufacturer sites
    # --------------------------------------------------------------------- #
    def vehicle_scraper(self) -> Agent:
        return Agent(
            role="Automotive Market Researcher",
            goal=(
                "Find brand-new petrol-powered cars below the user's budget, "
                "using ONLY official manufacturer websites, and return a clean dataset."
            ),
            backstory=dedent(
                """
                You are a meticulous researcher.  Third-party dealerships,
                review sites, and aggregators are **forbidden** sources.
                """
            ),
            llm=self.llm,
            allow_delegation=False,
        )

    # --------------------------------------------------------------------- #
    # 2) Agent that RANKS the scraped vehicles
    # --------------------------------------------------------------------- #
    def ranking_analyst(self) -> Agent:
        return Agent(
            role="Data-Driven Automotive Analyst",
            goal=(
                "Analyse a dataset of candidate cars, compute fair value metrics, "
                "and recommend the best buys."
            ),
            backstory=dedent(
                """
                You love combining horsepower, fuel economy, and price into
                objective scores.  Your outputs are short, numeric, and actionable.
                """
            ),
            tools=[PythonREPL()],
            llm=self.llm,
            allow_delegation=False,
        )
