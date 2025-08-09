from typing import Any, Union
from crewai import Task
from logger.logger import logger
from config import task_prompts as prompts

class TaskInitError(Exception):
    pass

def _validate_location(location: Any) -> str:
    if not isinstance(location, str) or not location.strip():
        raise TaskInitError("`location` must be a non-empty string.")
    return location.strip()

def _validate_budget(budget: Union[str, int, float]) -> str:
    if isinstance(budget, (int, float)):
        if budget <= 0:
            raise TaskInitError("`budget` must be greater than 0.")
        return str(int(budget))
    if not isinstance(budget, str) or not budget.strip():
        raise TaskInitError("`budget` must be numeric or a numeric-like string.")
    cleaned = budget.strip().replace(",", "").replace("$", "")
    try:
        val = float(cleaned)
    except ValueError as e:
        raise TaskInitError(f"`budget` must be numeric. Got: {budget!r}") from e
    if val <= 0:
        raise TaskInitError("`budget` must be greater than 0.")
    return str(int(val))

def _safe_task(label: str, **kwargs) -> Task:
    try:
        t = Task(**kwargs)
        logger.info("Created task: %s", label)
        return t
    except Exception as e:
        logger.exception("Failed creating task: %s", label)
        raise TaskInitError(f"Task creation failed for {label}: {e}") from e

class VehicleRecommenderTasks:
    def __tip_section(self) -> str:
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def data_collect_task(self, agent, location: Any, budget: Union[str, int, float]) -> Task:
        loc = _validate_location(location)
        norm_budget = _validate_budget(budget)
        description = prompts.DATA_COLLECT_TASK["description"].format(
            location=loc, budget=norm_budget, tip_section=self.__tip_section()
        )
        return _safe_task(
            "data_collect_task",
            description=description,
            expected_output=prompts.DATA_COLLECT_TASK["expected_output"],
            agent=agent,
        )

    def vehicle_analyze_task(self, agent, vehicles_task: Task) -> Task:
        if not isinstance(vehicles_task, Task):
            raise TaskInitError("`vehicles_task` must be a Task from data_collect_task().")
        description = prompts.VEHICLE_ANALYZE_TASK["description"].format(
            tip_section=self.__tip_section()
        )
        return _safe_task(
            "vehicle_analyze_task",
            description=description,
            expected_output=prompts.VEHICLE_ANALYZE_TASK["expected_output"],
            agent=agent,
            context=[vehicles_task],
        )

    def select_best_task(self, agent, analyzed_task: Task, budget: Union[str, int, float]) -> Task:
        if not isinstance(analyzed_task, Task):
            raise TaskInitError("`analyzed_task` must be a Task from vehicle_analyze_task().")
        norm_budget = _validate_budget(budget)
        description = prompts.SELECT_BEST_TASK["description"].format(budget=norm_budget)
        return _safe_task(
            "select_best_task",
            description=description,
            expected_output=prompts.SELECT_BEST_TASK["expected_output"],
            agent=agent,
            context=[analyzed_task],
            markdown=True,
        )
