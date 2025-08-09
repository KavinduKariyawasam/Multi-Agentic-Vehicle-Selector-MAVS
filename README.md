# Multi‑Agentic Vehicle Selector (MAVS)

MAVS is an opinionated template for building vehicle recommendation systems with [CrewAI](https://docs.crewai.com/).  It leverages multiple collaborating agents to scrape manufacturer data, enrich vehicle specifications and ultimately recommend the top options within a given budget.

## Key improvements over the original example

- **Structured outputs with Pydantic**: tasks validate their results against `VehicleSpec` and `Recommendation` models, catching schema drift early.
- **Smaller models, lower costs**: the data and analysis agents run on 8B Llama models while the recommender uses a Mixtral‑sized model.
- **Domain guardrails**: the `GuardedWebsiteSearchTool` ensures only allowed manufacturer domains are queried.
- **Hierarchical execution**: by setting `process=Process.hierarchical` and using the recommender as the manager, the crew can dynamically delegate subtasks when needed.
- **Async tools**: the Serper search tool runs asynchronously to avoid blocking the event loop.
- **Configurable via environment**: place your API keys in a `.env` file (see `.env.example`).

## Setup

1. **Clone this repo** (or copy it alongside your own project).
2. **Install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment**

   Copy `.env.example` to `.env` and fill in your `GROQ_API_KEY`, `TOGETHER_API_KEY` and `SERPER_API_KEY`.

4. **Run**

   ```bash
   python -m crew
   ```

   By default the location is `USA` and the budget is `40000`. You can override via environment variables:

   ```bash
   DEFAULT_LOCATION=Canada DEFAULT_BUDGET=35000 python -m crew
   ```

## Architecture

The system comprises three specialised agents coordinating through CrewAI:

| Agent | Responsibility | LLM | Delegation |
|------|---------------|-----|------------|
| **Data Agent** | Scrape raw vehicle data (model, trim, MSRP) exclusively from manufacturer websites. | together_ai/meta‑llama‑8B | Delegation disabled |
| **Analyzer Agent** | Enrich each vehicle with technical specs like engine type, MPG and safety features. | together_ai/meta‑llama‑8B | Delegation enabled |
| **Recommender Agent (Manager)** | Rank vehicles against the budget, produce final recommendations and manage sub‑tasks in a hierarchical execution. | groq/mixtral‑8x7b‑v2 | Delegation enabled |

Each agent uses a **guarded website search tool** configured to only pull data from permitted domains (e.g., `toyota.com`).  A general purpose `search_internet` tool backed by Serper.dev is also available for background research.

## Customisation

- **Adding manufacturers**: adjust the `allowed_sites` list in `crew.py` and update the tool factory accordingly.
- **Extending the schema**: edit `models.py` to add new fields, then update `VehicleRecommenderTasks` to reflect those fields in the instructions.
- **Observability**: to trace and monitor runs, supply a `config` section to the `Crew` constructor (see CrewAI docs on Observability).

## Testing

Unit tests live in the `tests/` directory and can be run with `pytest`.  They mock out network calls so you don’t burn through API quotas during CI runs.