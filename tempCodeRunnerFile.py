    try:
        result = crew.kickoff() if hasattr(crew, "kickoff") else crew.run()
    except BadRequestError as e:
        # e.body contains Groq’s full JSON error payload
        print("Groq 400:", e.body)
        raise     