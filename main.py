import os
from crewai import Agent, Task, Crew, Process
# from langchain_openai import ChatOpenAI
# from decouple import config

from textwrap import dedent
from agents import VehicleSelectorAgents
from tasks import VehicleRecommenderTasks

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
        # custom_agent_2 = agents.agent_2_name()

        # Custom tasks include agent name and variables as input
        data_collect_task = tasks.data_collect_task(
            data_agent,
            self.var1,
            self.var2,
        )

        # custom_task_2 = tasks.task_2_name(
        #     custom_agent_2,
        # )

        # Define your custom crew here
        crew = Crew(
            agents=[data_agent],
            tasks=[data_collect_task],
            verbose=True,
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Welcome to Vehicle Recommender Crew!")
    print("-------------------------------")
    # location = input(dedent("""Enter location: """))
    # budget = input(dedent("""Enter budget: """))
    location = "USA"
    budget = "20000"
    
    custom_crew = VehicleRecommenderCrew(location, budget)
    result = custom_crew.run()
    print("\n\n########################")
    print("Here is you custom crew run result:")
    print("########################\n")
    print(result)