import os
from textwrap import dedent

from crewai import Agent
from crewai_tools import CodeInterpreterTool  
# from crewai.tools import PythonREPL
from langchain_groq import ChatGroq            # pip install langchain-groq

# from langchain_experimental.utilities import PythonREPL
# from langchain_experimental.tools.python.tool import PythonREPLTool
# from langchain_core.tools import Tool  # already installed as a langchain dependency

# python_repl_tool = Tool(
#     name="python_repl",
#     description=(
#         "Run arbitrary Python; remember to print(...) anything "
#         "you want returned."
#     ),
#     func=LangChainPythonREPL().run,
#  )
# python_repl_tool = PythonREPLTool() 
class CustomAgents:
    """Factory for the two agents used in this project."""

    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set.  Put it in your shell or a .env file."
            )

        # One shared LLM instance keeps token-usage predictable
        # self.llm = ChatGroq(
        #     model_name="llama3-8b-8192",
        #     api_key=api_key,
        #     temperature=0.7,
        # )

        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.7   # ← kills the bad param
        )

    # --------------------------------------------------------------------- #
    # 1) Agent that SCRAPES manufacturer sites
    # --------------------------------------------------------------------- #
    def vehicle_scraper(self) -> Agent:
        """Returns the Automotive-Market-Researcher agent."""
        return Agent(
            role="Automotive Market Researcher",
            goal=(
                "Find brand-new petrol-powered cars below the user's budget, "
                "using ONLY official manufacturer websites, and return a clean dataset."
            ),
            backstory=dedent(
                """
                You are a meticulous researcher. Third-party dealerships,
                review sites, and aggregators are **forbidden** sources.
                """
            ),
            llm=self.llm,
            allow_delegation=False,
        )

    # --------------------------------------------------------------------- #
    # 2) Agent that RANKS the scraped vehicles
    # --------------------------------------------------------------------- #
    # ... inside CustomAgents.ranking_analyst()
    def ranking_analyst(self) -> Agent:
        return Agent(
            role="Data-Driven Automotive Analyst",
            goal=(
                "Analyse the dataset, compute fair-value metrics, "
                "and recommend the best buys."
            ),
            backstory=dedent(
                """
                You love turning raw specs into objective scores that balance
                price, performance, and efficiency. Work step-by-step, showing
                intermediate tables in your answer; you CANNOT execute code.
                """
            ),
            # 🚫  no tools list, no code_execution_mode
            llm=self.llm,
            allow_delegation=False,
        )