from textwrap import dedent

from crewai import Crew

from agents import CustomAgents
from tasks import CustomTasks


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
    result = crew.kickoff() if hasattr(crew, "kickoff") else crew.run()

    print("\n### Final Recommendations ###\n")
    print(result)


if __name__ == "__main__":
    main()
