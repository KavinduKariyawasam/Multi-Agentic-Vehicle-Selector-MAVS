import os
from crewai import Agent, Task, Crew, Process
# from langchain_openai import ChatOpenAI
# from decouple import config
import warnings
from textwrap import dedent
from agents import VehicleSelectorAgents
from tasks import VehicleRecommenderTasks

warnings.filterwarnings("ignore")

class VehicleRecommenderCrew:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = VehicleSelectorAgents()
        tasks = VehicleRecommenderTasks()

        # Define your custom agents and tasks here
        data_agent = agents.data_agent(allowed_sites=[
                                            "www.toyota.com"
                                            # , "www.ford.com", "automobiles.honda.com",
                                            # "www.chevrolet.com", "www.ramtrucks.com"
                                        ])
        vehicle_analyzer_agent = agents.vehicle_analyzer_agent()
        recommender_agent      = agents.vehicle_recommender_agent()

        # Custom tasks include agent name and variables as input
        data_collect_task = tasks.data_collect_task(
            data_agent,
            self.var1,
            self.var2,
        )

        vehicle_analyze_task = tasks.vehicle_analyze_task(
            vehicle_analyzer_agent,data_collect_task
        )

        select_best_task = tasks.select_best_task(
            recommender_agent,
            vehicle_analyze_task,
            self.var2   # budget
        )

        # Define your custom crew here
        crew = Crew(
            agents=[data_agent, vehicle_analyzer_agent, recommender_agent],
            tasks=[data_collect_task, vehicle_analyze_task, select_best_task],
            verbose=True,
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("Welcome to Vehicle Recommender Crew!")
    print("-------------------------------")
    # location = input(dedent("""Enter location: """))
    # budget = input(dedent("""Enter budget: """))
    location = "USA"
    budget = "40000"
    
    custom_crew = VehicleRecommenderCrew(location, budget)
    result = custom_crew.run()
    print("\n\n########################")
    print("Here is you custom crew run result:")
    print("########################\n")
    print(result)