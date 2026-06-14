from app.llm.llm_provider import generate_response


response = generate_response(
    "You are an incident response expert. "
    "What causes database connection pool exhaustion?"
)

print(response)