import warnings
from crewai import Agent, LLM
from textwrap import dedent
import requests
from groq import Groq
from dotenv import load_dotenv
import os
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool
from tools.search_tools import website_search_tool

warnings.filterwarnings("ignore", category=DeprecationWarning)

# SerperDevTool will read SERPER_API_KEY from the environment:
search_tool = ScrapeWebsiteTool(website_url='https://www.toyota.com')             # -> BaseTool

# Load from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

class VehicleSelectorAgents:
    def __init__(self):
        # self.search_tool = TavilySearch(max_results=5)
        self.groq_llm = LLM(model="groq/llama-3.3-70b-versatile")
        self.together_ai_llm = LLM(model="together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
                                    api_key=os.environ.get("TOGETHER_API_KEY"),
                                    base_url="https://api.together.xyz/v1"
                                    )
        self.website_search_tool = website_search_tool(website='https://www.toyota.com')

    def data_agent(self, allowed_sites=None):
        return Agent(
            role="Official Manufacturer Site Data Agent",
            backstory=dedent(f"""
                Purpose-built to extract and normalize vehicle specifications directly
                only from toyota.com.
                It executes JavaScript, navigates menus/configurators, and ignores
                ads, dealer inventory, or third-party listings.
            """),
            goal=dedent(f"""
                Gather real-time data on every brand-new vehicle model the OEM lists, regardless of fuel type or body style.
                For each model & trim, capture: year and MSRP.
                Output one JSON object per vehicle/trim (see schema below).
                Use only official manufacturer domains supplied in `allowed_sites`
                (or an internal whitelist if none supplied).
            """),
            tools=[self.website_search_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.together_ai_llm,
            extra_state={"allowed_sites": allowed_sites or []}
        )


    def vehicle_analyzer_agent(self):
        return Agent(
            role="Vehicle Specification Extraction Agent",
            backstory=dedent(f"""
            This agent is designed to extract comprehensive technical specifications
            for each vehicle model and trim provided by the data_collect_task.
            It focuses on gathering accurate details such as engine type, transmission,
            fuel efficiency, and key safety features, strictly from official U.S. automotive manufacturer sources.
            """),
            goal=dedent(f"""
            For every vehicle in the input list, collect and structure detailed specifications:
            - Engine type
            - Transmission type
            - Fuel efficiency (MPG or equivalent)
            - Key safety features

            Use only official U.S. manufacturer sources for all information.
            Output the results as a list of JSON objects, each representing a vehicle with its specifications.
            """),
            tools=[self.website_search_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.together_ai_llm,
        )
    
    def vehicle_recommender_agent(self):
        return Agent(
            role="Vehicle Recommendation Agent",
            backstory=dedent("""
               An automotive analyst who ranks options against a budget,
                balancing cost, efficiency, and safety, and explains the trade-offs
                in plain English.
            """),
            goal="Produce the top 3 recommendations and a concise, transparent analysis.",
            llm=self.groq_llm,
            verbose=True,
            allow_delegation=False,
        )