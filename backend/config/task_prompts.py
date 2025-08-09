from textwrap import dedent

OUTPUT_SCHEMA = dedent("""
{
    "year": "number",
    "model_name": "string",
    "trim": "string",
    "price": "number"
}
""").strip()

DATA_COLLECT_TASK = {
    "description": dedent("""
        Search only the official U.S. websites of automotive manufacturers to compile a list 
        of vehicles priced below **${budget} USD**. 
        
        Requirements:
        - Search within the location: {location}
        - Extract model names, available trims, engine specifications, and official MSRP
        - Exclude any third-party marketplaces, dealership aggregators, or review sites

        {tip_section}

        Use this variable: {location}
        And also this variable: {budget}
    """).strip(),
    "expected_output": f"A list of JSON objects with {OUTPUT_SCHEMA}"
}

VEHICLE_ANALYZE_TASK = {
    "description": dedent("""
        Take the input from data_collect_task (a list of vehicles) and, for each vehicle, gather detailed specifications:
        - Engine type
        - Transmission type
        - Fuel efficiency (MPG or equivalent)
        - Key safety features

        Only use official U.S. automotive manufacturer sources for this information.

        {tip_section}

        Provide the specifications in a structured JSON format for each vehicle.
    """).strip(),
    "expected_output": dedent("""
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
    """).strip()
}

SELECT_BEST_TASK = {
    "description": dedent("""
        You are the final recommender.

        ### How to read each vehicle
        * **Price** → `pricing.msrp`
        * **MPG**   → `fuelEconomy.combinedMpg`  
          (treat 0 as worst)
        * **#Safety**→ `len(features.safety)`
        * **Trim**  → `identification.trim`

        ### Scoring rubric
        1. price ≤ budget (hard filter; budget = {budget})
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
    """).strip(),
    "expected_output": "The JSON block above"
}
