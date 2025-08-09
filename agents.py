import os
from textwrap import dedent

from crewai import Agent, LLM

from .tools.search import create_manufacturer_search_tool, AsyncSerperSearchTool


class VehicleSelectorAgents:
    """
    Factory class responsible for constructing all of the agents used in the crew.
    Each agent is parameterised with its own persona, LLM and tools.
    """

    def __init__(self):
        # Use smaller models for data and analysis to reduce cost and latency.
        self.together_llm = LLM(
            model="together_ai/meta-llama/Llama-3.3-8B-Instruct",
            api_key=os.getenv("TOGETHER_API_KEY"),
            base_url="https://api.together.xyz/v1",
        )
        # Reserve a bigger model for the recommender for final reasoning.
        self.groq_llm = LLM(model="groq/mixtral-8x7b-v2")
        # Shared tools
        self.manufacturer_search_tool = create_manufacturer_search_tool(
            website="https://www.toyota.com",
            allowed_domains=["toyota.com"],
        )
        self.serper_tool = AsyncSerperSearchTool()

    def data_agent(self, allowed_sites: list[str] | None = None) -> Agent:
        """
        Agent that gathers raw vehicle data directly from official manufacturer sites.
        """
        return Agent(
            role="Official Manufacturer Site Data Agent",
            backstory=dedent(
                """
                Purpose‑built to extract and normalise vehicle specifications directly
                from manufacturer websites. It executes JavaScript, navigates menus,
                and ignores ads, dealer inventory or third‑party listings.
                """
            ),
            goal=dedent(
                """
                Gather real‑time data on every brand‑new vehicle model the OEM lists,
                regardless of fuel type or body style. For each model & trim, capture:
                year and MSRP. Use only official manufacturer domains supplied in
                `allowed_sites` (or the internal whitelist if none supplied).
                """
            ),
            tools=[self.manufacturer_search_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.together_llm,
            extra_state={"allowed_sites": allowed_sites or ["toyota.com"]},
        )

    def vehicle_analyzer_agent(self) -> Agent:
        """
        Agent dedicated to enriching raw vehicle lists with detailed specifications.
        """
        return Agent(
            role="Vehicle Specification Extraction Agent",
            backstory=dedent(
                """
                Designed to extract comprehensive technical specifications for each
                vehicle model and trim provided by the data collection stage. It
                focuses on gathering accurate details such as engine type,
                transmission, fuel efficiency and key safety features, strictly from
                official automotive manufacturer sources.
                """
            ),
            goal=dedent(
                """
                For every vehicle in the input list, collect and structure detailed
                specifications: price, engine type, transmission type, fuel efficiency
                (MPG or equivalent) and key safety features. Use only official
                manufacturer sources. Output the results as a list of VehicleSpec
                objects.
                """
            ),
            tools=[self.manufacturer_search_tool],
            allow_delegation=True,
            verbose=True,
            llm=self.together_llm,
        )

    def vehicle_recommender_agent(self) -> Agent:
        """
        Final agent responsible for ranking vehicles against the budget and
        articulating the trade‑offs to the user.
        """
        return Agent(
            role="Vehicle Recommendation Agent",
            backstory=dedent(
                """
                An automotive analyst who ranks options against a budget, balancing
                cost, efficiency and safety, and explains the trade‑offs in plain
                English.
                """
            ),
            goal="Produce the top 3 recommendations and a concise, transparent analysis.",
            llm=self.groq_llm,
            verbose=True,
            allow_delegation=True,
        )