import os
from crewai import Crew, Process
from .agents import VehicleSelectorAgents
from .tasks import VehicleRecommenderTasks


class VehicleRecommenderCrew:
    """
    Top‑level orchestrator for the Multi‑Agentic Vehicle Selector (MAVS).
    It wires agents and tasks together and kicks off execution using a
    hierarchical process for improved efficiency.
    """

    def __init__(self, location: str, budget: int):
        self.location = location
        self.budget = int(budget)

    def run(self):
        agents_factory = VehicleSelectorAgents()
        tasks_factory = VehicleRecommenderTasks()

        # Construct agents
        data_agent = agents_factory.data_agent(allowed_sites=["toyota.com"])
        analyzer_agent = agents_factory.vehicle_analyzer_agent()
        recommender_agent = agents_factory.vehicle_recommender_agent()

        # Construct tasks
        data_collect = tasks_factory.data_collect_task(
            data_agent, self.location, self.budget
        )
        analyze_task = tasks_factory.vehicle_analyze_task(
            analyzer_agent, data_collect
        )
        select_best = tasks_factory.select_best_task(
            recommender_agent, analyze_task, self.budget
        )

        # Compose the crew with a hierarchical process and a manager agent.
        crew = Crew(
            agents=[data_agent, analyzer_agent, recommender_agent],
            tasks=[data_collect, analyze_task, select_best],
            process=Process.hierarchical,
            manager_llm=None,  # fallback to default (the manager agent's LLM)
            manager_agent=recommender_agent,
            verbose=True,
        )

        return crew.kickoff()


if __name__ == "__main__":
        print("Welcome to MAVS!")
        location = os.environ.get("DEFAULT_LOCATION", "USA")
        budget = int(os.environ.get("DEFAULT_BUDGET", "40000"))
        crew = VehicleRecommenderCrew(location, budget)
        result = crew.run()
        print(result)