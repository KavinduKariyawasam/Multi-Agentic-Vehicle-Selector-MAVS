# To know more about the Task class, visit: https://docs.crewai.com/concepts/tasks
from crewai import Task
from textwrap import dedent

# OUTPUT_SCHEMA = dedent("""
#     {
#         "year": "number",
#         "model_name": "string",
#         "trim": "string",
#         "price": "number"
#     }
# """)

OUTPUT_SCHEMA =  dedent("""
{
    "identification": {
      "description": "Basic identification details for the vehicle.",
      "type": "object",
      "properties": {
        "make": { "type": "string", "description": "The manufacturer of the vehicle (e.g., Toyota, Ford)." },
        "model": { "type": "string", "description": "The model name of the vehicle (e.g., Camry, Mustang)." },
        "year": { "type": "integer", "description": "The model year of the vehicle." },
        "trim": { "type": "string", "description": "The specific trim level (e.g., LE, XLT, Sport)." },
        "bodyStyle": { "type": "string", "description": "The body style of the vehicle (e.g., Sedan, SUV, Coupe)." }
      }
    },
    "pricing": {
      "description": "Pricing information for the vehicle.",
      "type": "object",
      "properties": {
        "msrp": { "type": "number", "description": "Manufacturer's Suggested Retail Price in USD." },
        "destinationCharge": { "type": "number", "description": "Fees for transporting the vehicle to the dealer." }
      }
    },
    "engineAndPerformance": {
      "description": "Details about the engine and vehicle performance.",
      "type": "object",
      "properties": {
        "engineType": { "type": "string", "description": "Description of the engine (e.g., 2.5L 4-Cylinder, Electric Motor)." },
        "horsepower": { "type": "integer", "description": "Peak horsepower." },
        "torque": { "type": "integer", "description": "Peak torque in lb-ft." },
        "transmission": { "type": "string", "description": "Type of transmission (e.g., 8-Speed Automatic, CVT)." },
        "drivetrain": { "type": "string", "enum": ["FWD", "RWD", "AWD", "4WD"], "description": "Drivetrain type." }
      }
    },
    "fuelEconomy": {
      "description": "Fuel efficiency information for all fuel types.",
      "type": "object",
      "properties": {
        "fuelType": { "type": "string", "enum": ["Gasoline", "Diesel", "Hybrid", "Electric", "Plug-in Hybrid"] },
        "cityMpg": { "type": "integer", "description": "EPA-estimated city miles per gallon (for non-electric)." },
        "highwayMpg": { "type": "integer", "description": "EPA-estimated highway miles per gallon (for non-electric)." },
        "combinedMpg": { "type": "integer", "description": "EPA-estimated combined miles per gallon (for non-electric)." },
        "epaRangeMi": { "type": "integer", "description": "EPA-estimated range in miles (for electric)." },
        "batteryCapacityKwh": { "type": "number", "description": "Battery capacity in kWh (for electric)." }
      }
    },
    "dimensions": {
      "description": "Exterior and interior dimensions and weights.",
      "type": "object",
      "properties": {
        "lengthIn": { "type": "number" }, "widthIn": { "type": "number" }, "heightIn": { "type": "number" },
        "wheelbaseIn": { "type": "number" }, "curbWeightLbs": { "type": "integer" }, "cargoVolumeFt3": { "type": "number" }
      }
    },
    "capacities": {
      "description": "Seating and fluid capacities.",
      "type": "object",
      "properties": {
        "seating": { "type": "integer" },
        "fuelTankGal": { "type": "number", "description": "Fuel tank capacity in gallons." }
      }
    },
    "features": {
      "description": "Lists of key features.",
      "type": "object",
      "properties": {
        "exterior": { "type": "array", "items": { "type": "string" } },
        "interior": { "type": "array", "items": { "type": "string" } },
        "safety": { "type": "array", "items": { "type": "string" } }
      }
    },
    "colors": {
      "description": "Available color options.",
      "type": "object",
      "properties": {
        "exterior": { "type": "array", "items": { "type": "object", "properties": { "name": { "type": "string" }, "hexCode": { "type": "string" } } } },
        "interior": { "type": "array", "items": { "type": "object", "properties": { "name": { "type": "string" }, "material": { "type": "string" } } } }
      }
    },
    "warranty": {
      "description": "Manufacturer warranty information.",
      "type": "object",
      "properties": {
        "basic": { "type": "string", "description": "e.g., '3 years / 36,000 miles'" },
        "powertrain": { "type": "string", "description": "e.g., '5 years / 60,000 miles'" }
      }
    }
}
""")


class VehicleRecommenderTasks:
    """All tasks in the crew share this one schema."""

    # ----------------------------------------------------------
    # Private helper
    # ----------------------------------------------------------
    def _tip(self) -> str:
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    # ----------------------------------------------------------
    # 1️⃣  Collect base data
    # ----------------------------------------------------------
    def data_collect_task(self, agent, location: str, budget: int):
        return Task(
            description=dedent(f"""
                Search **official U.S. manufacturer websites only** and return
                vehicles whose **pricing.msrp ≤ ${budget}**.

                * Do **NOT** include third-party marketplaces or reviews.
                * Return each vehicle exactly once using the schema below.

                {self._tip()}

                ```json
                {OUTPUT_SCHEMA}
                ```
            """),
            expected_output="A JSON list where every object matches the schema above",
            agent=agent,
        )

    # ----------------------------------------------------------
    # 2️⃣  Enrich each vehicle with specs
    # ----------------------------------------------------------
    def vehicle_analyze_task(self, agent, vehicles_task: Task):
        return Task(
            description=dedent(f"""
                For each vehicle in **context**, add:

                • `engineAndPerformance.engineType`
                • `engineAndPerformance.transmission`
                • `fuelEconomy.*` fields (MPG or electric range)
                • `features.safety` list

                Use only official manufacturer sources.

                {self._tip()}
            """),
            expected_output=(
                "A JSON list, same schema as input, now **including** the new "
                "engine, MPG, and safety details."
            ),
            agent=agent,
            context=[vehicles_task],               # pass upstream output  :contentReference[oaicite:2]{index=2}
        )

    # ----------------------------------------------------------
    # 3️⃣  Pick the best three and explain
    # ----------------------------------------------------------
    def select_best_task(self, agent, analyzed_task: Task, budget: int):
        return Task(
            description=dedent(f"""
                You are the final recommender.

                ### How to read each vehicle
                * **Price** → `pricing.msrp`
                * **MPG**   → `fuelEconomy.combinedMpg`  
                  (treat 0 as worst)
                * **#Safety**→ `len(features.safety)`
                * **Trim**  → `identification.trim`

                ### Scoring rubric
                1. price ≤ budget (hard filter)
                2. higher MPG ⇒ higher rank
                3. more safety features ⇒ higher rank
                4. newer model year breaks ties

                ### Output (exactly)
                ```json
                {{
                  "top_picks": [
                    {{ "rank": 1, "model_name": "...", "trim": "...", "price": ..., "key_reason": "..." }},
                    {{ "rank": 2, "model_name": "...", "trim": "...", "price": ..., "key_reason": "..." }},
                    {{ "rank": 3, "model_name": "...", "trim": "...", "price": ..., "key_reason": "..." }}
                  ],
                  "analysis": "150-250 word comparison explaining why #1 outranks #2 and #3"
                }}
                ```
            """),
            expected_output="The JSON block above",
            agent=agent,
            context=[analyzed_task],
            markdown=True
        )