from crewai import Agent, LLM
from textwrap import dedent
import requests
from groq import Groq
from dotenv import load_dotenv
import os
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool

# SerperDevTool will read SERPER_API_KEY from the environment:
search_tool = ScrapeWebsiteTool(website_url='https://www.toyota.com')             # -> BaseTool

# Load from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

class VehicleSelectorAgents:
    def __init__(self):
        # self.search_tool = TavilySearch(max_results=5)
        self.groq_llm = LLM(model="groq/llama-3.3-70b-versatile")
        self.website_search_tool = WebsiteSearchTool(config=dict(
                                                        llm=dict(
                                                        provider="groq", # or google, openai, anthropic, llama2, ...
                                                        config=dict(
                                                            model="llama-3.3-70b-versatile",
                                                            # temperature=0.5,
                                                            # top_p=1,
                                                            # stream=true,
                                                        ),
                                                        ),
                                                        embedder = dict(
                                                            provider = "huggingface",        # local sentence-transformers
                                                            config = dict(
                                                                model = "sentence-transformers/all-MiniLM-L6-v2",
                                                                # task_type = "retrieval_document",
                                                            ),
                                                        ),
                                                    )
                                                )

    def data_agent(self, allowed_sites=None):
        return Agent(
            role="Official Manufacturer Site Data Agent",
            backstory=dedent(f"""
                Purpose-built to extract and normalize vehicle specifications directly
                from automakers' own U.S. websites (e.g., toyota.com, automobiles.honda.com).
                It executes JavaScript, navigates menus/configurators, and ignores
                ads, dealer inventory, or third-party listings.
            """),
            goal=dedent(f"""
                • Gather real-time data on every brand-new vehicle model the OEM lists,
                regardless of fuel type or body style.
                • For each model & trim, capture: year, body_style, fuel_type,
                powertrain/engine, drivetrain, transmission, key features, and MSRP.
                • Output one JSON object per vehicle/trim (see schema below).
                • Use only official manufacturer domains supplied in `allowed_sites`
                (or an internal whitelist if none supplied).
            """),
            tools=[self.website_search_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.groq_llm,
            extra_state={"allowed_sites": allowed_sites or []}
        )


    def agent_2_name(self):
        return Agent(
            role="Define agent 2 role here",
            backstory=dedent(f"""Define agent 2 backstory here"""),
            goal=dedent(f"""Define agent 2 goal here"""),
            # tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            llm=self.groq_llm,
        )