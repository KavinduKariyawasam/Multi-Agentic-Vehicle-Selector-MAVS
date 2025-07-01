# To know more about the Task class, visit: https://docs.crewai.com/concepts/tasks
from crewai import Task
from textwrap import dedent


class CustomTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def data_collect_task(self, agent, location, budget):
        return Task(
            description=dedent(
                f"""
                Search only the official U.S. websites of automotive manufacturers to compile a list 
                of **brand-new petrol-powered cars** priced below **${budget} USD**. 
                
                Requirements:
                - Search within the location: {location}
                - Extract model names, available trims, engine specifications, and official MSRP
                - Ignore hybrid, electric, or diesel models unless clearly petrol options exist
                - Exclude any third-party marketplaces, dealership aggregators, or review sites

                {self.__tip_section()}

                Use this variable: {location}
                And also this variable: {budget}
            """
            ),
            expected_output="A clean table (JSON or DataFrame) listing qualifying petrol cars, their trims, engine details, and MSRP from only official manufacturer websites.",
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