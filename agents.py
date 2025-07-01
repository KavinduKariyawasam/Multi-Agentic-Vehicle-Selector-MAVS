from crewai import Agent, LLM
from textwrap import dedent
from langchain_community.llms import Ollama
# from langchain_openai import ChatOpenAI
# from langchain_core.language_models.llms import LLM
import requests
from groq import Groq
from dotenv import load_dotenv
import os
from langchain_tavily import TavilySearch
from tools.search_tools import SearchTools
from crewai_tools import ScrapeWebsiteTool
import os

# SerperDevTool will read SERPER_API_KEY from the environment:
search_tool = ScrapeWebsiteTool()             # -> BaseTool
# website_tool = WebsiteSearchTool()    
# Load from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

search_tools = SearchTools()                 # <-- instantiate
internet_search_tool = search_tools.search_internet 

class CustomAgents:
    def __init__(self):
        # self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        # self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        # self.groq_llm = Groq(api_key="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")
        # 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
        self.search_tool = TavilySearch(max_results=5)
        self.groq_llm = LLM(model="groq/llama-3.3-70b-versatile")

    def data_agent(self):
        return Agent(
            role="Official Manufacturer Site Data Agent",
            backstory=dedent(f"""
                This agent is designed to extract and standardize vehicle data **only** from official 
                automotive manufacturer websites (e.g., automobiles.honda.com, toyota.com). 
                It simulates user interactions, handles modern JavaScript-heavy pages, and is immune 
                to distractions from ads, dealer promos, or third-party listings.

                The agent was created to help streamline vehicle research by focusing purely 
                on the source-of-truth: the car makers themselves.
            """),
            goal=dedent(f"""
                To extract accurate, real-time information on brand-new petrol-powered vehicles 
                listed on official U.S. manufacturer websites. It collects vehicle models, trims, 
                engine types, features, and MSRP — while avoiding any third-party or dealer-based data.You can call one tool:

                • search_tool: Searches official automaker sites only. Avoid dealers and ads.
            """),
            tools=[search_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.groq_llm,
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