from textwrap import dedent

from crewai import Task


class CustomTasks:
    """Two tasks: scrape → analyse."""

    # ---------------------------------------------------------- #
    # Step 1 – Collect qualifying vehicles
    # ---------------------------------------------------------- #
    def collect_vehicles(self, agent, location: str, budget: float) -> Task:
        return Task(
            description=dedent(
                f"""
                Search ONLY official manufacturer websites to list **brand-new petrol cars**
                priced under **${budget:,.0f} USD** and available in **{location}**.

                Record for every model:
                • brand & model name
                • trim / grade
                • engine configuration & displacement
                • horsepower (hp) and EPA combined MPG
                • official MSRP in USD

                Exclude hybrid, electric, and diesel variants.  
                Exclude third-party dealership or review sites.

                **Return the data as either a Markdown table or plain CSV text —
                do NOT wrap it in JSON.**
                """
            ),
            expected_output=(
                "A Markdown or CSV table with columns "
                "[brand, model, trim, engine, hp, mpg, msrp_usd]"
            ),
            agent=agent,
        )

    # ---------------------------------------------------------- #
    # Step 2 – Rank the collected vehicles
    # ---------------------------------------------------------- #
    def rank_vehicles(self, agent, scraping_task: Task, top_n: int = 5) -> Task:
        return Task(
            description=dedent(
                f"""
                You will receive, as **context**, the dataset produced in Task 1.

                • Convert the input to a DataFrame (if needed).  
                • Compute:
                     horsepower_per_dollar = hp  / msrp_usd
                     mpg_per_dollar        = mpg / msrp_usd
                • Min-max scale these two metrics and average them
                  into an 'overall' score.  
                • Sort descending by 'overall'.

                Return:
                  1. The full ranked table (same columns + 'overall').  
                  2. A concise bullet-point explanation of the **Top {top_n}**.

                Keep the narrative crisp and data-driven.
                """
            ),
            expected_output=(
                "A table sorted by 'overall' plus a short narrative discussing the Top picks."
            ),
            agent=agent,
            context=[scraping_task],  # ← new CrewAI “context” pattern
        )
