# To know more about the Task class, visit: https://docs.crewai.com/concepts/tasks
from crewai import Task
from textwrap import dedent

OUTPUT_SCHEMA = dedent("""
    {
        "year": "number",
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

    def vehicle_analyze_task(self, agent,vehicles_task):
        return Task(
            description=dedent(
            f"""
            Take the input from data_collect_task (a list of vehicles) and, for each vehicle, gather detailed specifications:
            - Engine type
            - Transmission type
            - Fuel efficiency (MPG or equivalent)
            - Key safety features

            Only use official U.S. automotive manufacturer sources for this information.

            {self.__tip_section()}

            Provide the specifications in a structured JSON format for each vehicle.
            """
            ),
            expected_output=dedent("""
            A list of JSON objects, each containing:
            {
                "year": "number",
                "model_name": "string",
                "price": "number",
                "trim": "string",
                "engine_type": "string",
                "transmission_type": "string",
                "fuel_efficiency": "string",
                "safety_features": ["string", ...]
            }
            """),
            agent=agent,
            context=[vehicles_task]
        )