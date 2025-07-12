# To know more about the Task class, visit: https://docs.crewai.com/concepts/tasks
from crewai import Task
from textwrap import dedent

OUTPUT_SCHEMA = dedent("""
    {
        "model_name": "string",
        "trim": "string",
        "price": "number"
    }
""")

class VehicleRecommenderTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def data_collect_task(self, agent, location, budget):
        return Task(
            description=dedent(
                f"""
                Search only the official U.S. websites of automotive manufacturers to compile a list 
                of vehicles priced below **${budget} USD**. 
                
                Requirements:
                - Search within the location: {location}
                - Extract model names, available trims, engine specifications, and official MSRP
                - Exclude any third-party marketplaces, dealership aggregators, or review sites

                {self.__tip_section()}

                Use this variable: {location}
                And also this variable: {budget}
            """
            ),
            expected_output=f"A list of JSON objects with {OUTPUT_SCHEMA}",
            agent=agent,
        )

    def task_2_name(self, agent):
        return Task(
            description=dedent(
                f"""
            Take the input from task 1 and do something with it.
                                       
            {self.__tip_section()}

            Make sure to do something else.
        """
            ),
            expected_output="The expected output of the task",
            agent=agent,
        )