from textwrap import dedent

from crewai import Crew

from agents import CustomAgents
from tasks import CustomTasks

# from crewai.llm import BadRequestError
try:                                   # openai ≥ 1.0
    from openai import BadRequestError
except ImportError:                    # openai 0.27-0.28
    from openai.error import InvalidRequestError as BadRequestError

def main() -> None:
    print("### Vehicle-Finder Crew\n")

    # ------------------------------------------------------------------ #
    # Simple interactive CLI
    # ------------------------------------------------------------------ #
    location = input("Enter sales region / country (e.g. 'United States'): ").strip()
    budget   = float(
        input("Enter maximum budget in USD (e.g. 30000): ").replace(",", "").strip()
    )

    # ------------------------------------------------------------------ #
    # Instantiate agents & tasks
    # ------------------------------------------------------------------ #
    agents = CustomAgents()
    tasks  = CustomTasks()

    scraper_agent = agents.vehicle_scraper()
    analyst_agent = agents.ranking_analyst()

    task_scrape = tasks.collect_vehicles(scraper_agent, location, budget)
    task_rank   = tasks.rank_vehicles(analyst_agent, task_scrape)

    crew = Crew(
        agents=[scraper_agent, analyst_agent],
        tasks=[task_scrape, task_rank],
        verbose=True,
    )

    # CrewAI ≤ 0.24 uses .kickoff(); ≥ 0.25 switched to .run()
    # --- wherever you run the crew ----------------------------------------
    try:
        result = crew.kickoff() if hasattr(crew, "kickoff") else crew.run()
    except BadRequestError as e:
        # new SDK ⇒ e.response; old SDK ⇒ e.body
        payload = getattr(e, "response", None) or getattr(e, "body", None)
        if hasattr(payload, "text"):           # requests.Response
            print("Groq 400 →", payload.status_code, payload.text)
        else:
            print("Groq 400 →", payload or str(e))
        raise
                             # optional: re-raise for traceback

    print("\n### Final Recommendations ###\n")
    print(result)


if __name__ == "__main__":
    main()
