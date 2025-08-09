# agents.py
import os
import warnings
from typing import List, Optional
from crewai import Agent, LLM
from dotenv import load_dotenv 

from logger.logger import logger
from config import agent_prompts as prompts  # <-- new import

warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv() 

class AgentInitError(Exception):
    pass

def _require_env(name: str, allow_empty: bool = False) -> str:
    val = os.getenv(name)
    if not allow_empty and (val is None or not str(val).strip()):
        raise AgentInitError(f"Missing required environment variable: {name}")
    return val.strip()

def _safe_llm(label: str, **kwargs) -> LLM:
    try:
        llm = LLM(**kwargs)
        logger.info("Initialized LLM for %s (model=%s)", label, kwargs.get("model"))
        return llm
    except Exception as e:
        logger.exception("Failed to initialize LLM for %s", label)
        raise AgentInitError(f"LLM init failed for {label}: {e}") from e

def _get_tool():
    # Your existing factory import (kept lazy to avoid import cycles)
    try:
        from tools.search_tools import website_search_tool
    except Exception as e:
        raise AgentInitError(f"Unable to import website_search_tool: {e}") from e
    try:
        return website_search_tool()
    except Exception as e:
        raise AgentInitError(f"website_search_tool() failed: {e}") from e

class VehicleSelectorAgents:
    def __init__(self) -> None:
        self.groq_model = _require_env("GROQ_MODEL")
        self.groq_api_key = os.getenv("GROQ_API_KEY")  # optional

        self.together_model = _require_env("TOGETHER_MODEL")
        self.together_api_key = _require_env("TOGETHER_API_KEY")
        self.together_base_url = _require_env("TOGETHER_BASE_URL")

        self.groq_llm = _safe_llm(
            "groq_llm",
            model=self.groq_model,
            api_key=self.groq_api_key if self.groq_api_key else None,
        )
        self.together_ai_llm = _safe_llm(
            "together_ai_llm",
            model=self.together_model,
            api_key=self.together_api_key,
            base_url=self.together_base_url,
        )

        self.website_search_tool = _get_tool()

    def data_agent(self, allowed_sites: Optional[List[str]] = None) -> Agent:
        try:
            return Agent(
                role=prompts.DATA_AGENT["role"],
                backstory=prompts.DATA_AGENT["backstory"],
                goal=prompts.DATA_AGENT["goal"],
                tools=[self.website_search_tool],
                allow_delegation=False,
                verbose=True,
                llm=self.together_ai_llm,
                extra_state={"allowed_sites": allowed_sites or []},
            )
        except Exception as e:
            logger.exception("Failed to create data_agent")
            raise AgentInitError(f"data_agent creation failed: {e}") from e

    def vehicle_analyzer_agent(self) -> Agent:
        try:
            return Agent(
                role=prompts.VEHICLE_ANALYZER_AGENT["role"],
                backstory=prompts.VEHICLE_ANALYZER_AGENT["backstory"],
                goal=prompts.VEHICLE_ANALYZER_AGENT["goal"],
                tools=[self.website_search_tool],
                allow_delegation=False,
                verbose=True,
                llm=self.together_ai_llm,
            )
        except Exception as e:
            logger.exception("Failed to create vehicle_analyzer_agent")
            raise AgentInitError(f"vehicle_analyzer_agent creation failed: {e}") from e

    def vehicle_recommender_agent(self) -> Agent:
        try:
            return Agent(
                role=prompts.VEHICLE_RECOMMENDER_AGENT["role"],
                backstory=prompts.VEHICLE_RECOMMENDER_AGENT["backstory"],
                goal=prompts.VEHICLE_RECOMMENDER_AGENT["goal"],
                llm=self.groq_llm,
                verbose=True,
                allow_delegation=False,
            )
        except Exception as e:
            logger.exception("Failed to create vehicle_recommender_agent")
            raise AgentInitError(f"vehicle_recommender_agent creation failed: {e}") from e
