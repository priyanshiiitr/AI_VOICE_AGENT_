from fastapi import FastAPI
from agent.llm_agent import generate_response

app = FastAPI()


@app.get("/")
def health():

    return {"status": "voice agent running"}


@app.post("/chat")
async def chat(user_input: str):

    reply = generate_response(user_input)

    return {
        "user": user_input,
        "agent": reply
    }