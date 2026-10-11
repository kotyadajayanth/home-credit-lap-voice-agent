# chat_with_prompt.py
# OPTIONAL: lets you chat with the real system prompt in the terminal
# (text only) before pasting it into Retell / Bolna.
# Needs an Anthropic API key in the .env file.
# Run:  python src/chat_with_prompt.py

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
model_name = os.getenv("MODEL_NAME", "claude-sonnet-5-5")

if not api_key:
    print("Please add ANTHROPIC_API_KEY in the .env file first.")
    raise SystemExit

# values for the prompt variables (change these to test)
variables = {
    "company_name": "Home Credit",
    "customer_name": "Rahul Sharma",
    "agent_name": "Priya",
    "agent_gender": "female",
    "current_date": "10 October 2026",
    "current_day": "Saturday",
    "current_time": "11:00 AM",
    "additional_context_from_rag": "No extra product information available.",
    "language_to_speak": "English",
    # these two are handled by the chat messages below
    "conversation_history": "(see messages)",
    "customer_utterance": "(see messages)",
}

with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

for name, value in variables.items():
    system_prompt = system_prompt.replace("{{" + name + "}}", value)

client = anthropic.Anthropic(api_key=api_key)
messages = []

print("Type what the customer says. Type 'quit' to stop.\n")

# the agent speaks first, so we send a starting message
messages.append({"role": "user", "content": "(call connected)"})

while True:
    reply = client.messages.create(
        model=model_name,
        max_tokens=300,
        system=system_prompt,
        messages=messages,
    )
    agent_text = reply.content[0].text
    print("Agent:", agent_text)
    messages.append({"role": "assistant", "content": agent_text})

    customer_text = input("You: ")
    if customer_text.lower() == "quit":
        break
    messages.append({"role": "user", "content": customer_text})
