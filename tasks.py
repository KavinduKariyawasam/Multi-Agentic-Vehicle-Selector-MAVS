from crewai import Task
from textwrap import dedent

from .models import VehicleSpec, Recommendation, TopPick  # for type hints only


class VehicleRecommenderTasks:
    """
    Builder class encapsulating each unit of work in the vehicle recommendation flow.
    Tasks accept agents and runtime parameters and return Task objects.
    """

    def data_collect_task(self, agent, location: str, budget: int) -> Task:
        """
        Create a task that compiles a list of vehicles below a specified budget.
        """
        return Task(
            description=dedent(
                f"""
                Search only the official manufacturer websites to compile a list of
                vehicles priced below ${budget} USD in {location}. Extract model names,
                available trims, engine specifications and official MSRP. Exclude any
                third‑party marketplaces, dealership aggregators or review sites.

                Location: {location}
                Budget: ${budget}
                """
            ),
            agent=agent,
            # This instructs CrewAI to validate the output using the VehicleSpec model.
            output_pydantic=VehicleSpec,
            expected_output="A list of VehicleSpec objects, one per vehicle.",
        )

    def vehicle_analyze_task(self, agent, vehicles_task: Task) -> Task:
        """
        Create a task that enriches a list of vehicles with full technical specs.
        """
        return Task(
            description=dedent(
                """
                Take the list of vehicles from the data collection stage and, for each
                vehicle, gather detailed specifications: engine type, transmission type,
                fuel efficiency (MPG or MPGe) and key safety features. Only use official
                automotive manufacturer sources. Provide the results as a list of
                VehicleSpec objects (the existing objects enriched with additional fields).
                """
            ),
            agent=agent,
            context=[vehicles_task],
            output_pydantic=VehicleSpec,
            expected_output="An updated list of VehicleSpec objects with full specifications.",
        )

    def select_best_task(self, agent, analyzed_task: Task, budget: int) -> Task:
        """
        Create a task that ranks vehicles against the budget using a transparent rubric.
        """
        return Task(
            description=dedent(
                f"""
                You are the final recommender.

                ### Scoring rubric
                1. price ≤ {budget} (hard filter)
                2. higher MPG ⇒ higher rank
                3. more safety features ⇒ higher rank
                4. newer model year breaks ties

                ### Output
                Provide the final result as a Recommendation object. It must contain:
                - top_picks: A list of 3 TopPick objects with rank, model_name, trim,
                  price and a succinct key_reason explaining why each vehicle is in that
                  position.
                - analysis: A 150–250 word narrative explaining why the #1 pick outranks
                  #2 and #3, highlighting trade‑offs between cost, efficiency and safety.
                """
            ),
            agent=agent,
            context=[analyzed_task],
            output_pydantic=Recommendation,
            expected_output="A Recommendation object as described above.",
            markdown=True,
        )