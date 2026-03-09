import google.generativeai as genai
import json
from config.settings import GEMINI_API_KEY

from agent.tools import (
    book_table,
    get_menu,
    get_price,
    restaurant_hours,
    restaurant_location
)

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


SYSTEM_PROMPT = """
You are an AI restaurant receptionist.

You can use these tools:

get_menu()
get_price(item_name)
restaurant_hours()
restaurant_location()
book_table(name, people, time)

If a tool is required, respond ONLY in JSON like this:

{
 "tool": "tool_name",
 "arguments": { }
}

Otherwise respond normally.
"""


def generate_response(user_text):

    prompt = SYSTEM_PROMPT + "\nUser: " + user_text

    response = model.generate_content(prompt)

    reply = response.text.strip()

    # Try parsing tool call
    try:
        data = json.loads(reply)

        tool = data["tool"]
        args = data.get("arguments", {})

        if tool == "get_menu":
            return get_menu()

        if tool == "get_price":
            return get_price(**args)

        if tool == "restaurant_hours":
            return restaurant_hours()

        if tool == "restaurant_location":
            return restaurant_location()

        if tool == "book_table":
            return book_table(**args)

    except:
        pass

    return reply