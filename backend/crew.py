import sys
import warnings
from textwrap import dedent

from agents import VehicleSelectorAgents
from tasks import VehicleRecommenderTasks
from crewai import Crew

from logger.logger import logger, set_log_level  # <-- shared logger import

warnings.filterwarnings("ignore")


class VehicleRecommenderError(Exception):
    pass


class ValidationError(VehicleRecommenderError):
    pass


def _validate_location(location):
    if not isinstance(location, str) or not location.strip():
        raise ValidationError("`location` must be a non-empty string.")
    return location.strip()


def _validate_budget(budget):
    if isinstance(budget, (int, float)):
        if budget <= 0:
            raise ValidationError("`budget` must be greater than 0.")
        return str(int(budget))

    if not isinstance(budget, str) or not budget.strip():
        raise ValidationError("`budget` must be numeric.")

    cleaned = budget.strip().replace(",", "").replace("$", "")
    try:
        val = float(cleaned)
    except ValueError as e:
        raise ValidationError(f"`budget` must be numeric. Got: {budget!r}") from e

    if val <= 0:
        raise ValidationError("`budget` must be greater than 0.")
    return str(int(val))


def _safe_call(label, fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.exception("Error during %s", label)
        raise VehicleRecommenderError(f"Failed during {label}: {e}") from e


class VehicleRecommenderCrew:
    def __init__(self, location, budget):
        self.location = _validate_location(location)
        self.budget = _validate_budget(budget)

    def run(self):
        logger.info("Starting VehicleRecommenderCrew with location=%s, budget=%s",
                    self.location, self.budget)

        agents = _safe_call("VehicleSelectorAgents creation", VehicleSelectorAgents)
        tasks = _safe_call("VehicleRecommenderTasks creation", VehicleRecommenderTasks)

        data_agent = _safe_call("data_agent creation", agents.data_agent)
        vehicle_analyzer_agent = _safe_call("vehicle_analyzer_agent creation", agents.vehicle_analyzer_agent)
        recommender_agent = _safe_call("vehicle_recommender_agent creation", agents.vehicle_recommender_agent)

        data_collect_task = _safe_call(
            "data_collect_task creation",
            tasks.data_collect_task,
            data_agent,
            self.location,
            self.budget,
        )

        vehicle_analyze_task = _safe_call(
            "vehicle_analyze_task creation",
            tasks.vehicle_analyze_task,
            vehicle_analyzer_agent,
            data_collect_task,
        )

        select_best_task = _safe_call(
            "select_best_task creation",
            tasks.select_best_task,
            recommender_agent,
            vehicle_analyze_task,
            self.budget,
        )

        crew = _safe_call(
            "Crew creation",
            Crew,
            agents=[data_agent, vehicle_analyzer_agent, recommender_agent],
            tasks=[data_collect_task, vehicle_analyze_task, select_best_task],
            verbose=True,
        )

        result = _safe_call("crew.kickoff()", crew.kickoff)

        logger.info("VehicleRecommenderCrew completed successfully.")
        return result


if __name__ == "__main__":
    try:
        print("Welcome to Vehicle Recommender Crew!")
        print("-------------------------------")

        location = input("Enter your location (e.g., 'USA, UK'): ")
        budget = input("Enter your budget (e.g., '40000'): ")

        custom_crew = VehicleRecommenderCrew(location, budget)
        result = custom_crew.run()

        print("\n\n########################")
        print("Here is your custom crew run result:")
        print("########################\n")
        print(result)

    except ValidationError as ve:
        logger.error("Invalid inputs: %s", ve)
        sys.exit(2)
    except VehicleRecommenderError as vre:
        logger.error("Application error: %s", vre)
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        sys.exit(1)
