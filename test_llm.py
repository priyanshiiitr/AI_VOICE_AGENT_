from agent.llm_agent import generate_response

while True:
    user = input("You: ")

    reply = generate_response(user)

    print("Agent:", reply)