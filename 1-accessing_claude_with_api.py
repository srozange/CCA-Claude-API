#!/usr/bin/env python3
from anthropic import Anthropic
import json

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=1.0, stop_sequences=None):
    with client.messages.stream(
        model=model,
        max_tokens=1000,
        messages=messages,
        system=system,
        temperature=temperature,
        stop_sequences=stop_sequences
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()
    return stream.get_final_message()

client = Anthropic()
model = "claude-haiku-4-5"

print("Choisissez une démo :")
print("  1. structured output")
print("  2. structured output (3 commands)")
print("  3. chatbot")
choice = input("Votre choix (1/2/3) : ").strip()

if choice == "1":
    messages = []
    add_user_message(messages, "Generate a very short event bridge rule as json")
    add_assistant_message(messages, "```json")
    print(chat(messages, system="", stop_sequences=["```"]))

elif choice == "2":
    messages = []
    add_user_message(messages, "Generate three different sample AWS CLI commands. Each should be very short")
    add_assistant_message(messages, "here are all 3 commands in a single block\n```bash")
    print(chat(messages, system="", stop_sequences=["```"]))

elif choice == "3":
    messages = []
    while True:
        user_input = input("> ")
        add_user_message(messages, user_input)
        system = """
    You are a patient math tutor.
    Do not directly answer a student's questions.
    Guide them to a solution step by step.
    """
        answer = chat(messages, system=system)
        add_assistant_message(messages, answer.content[0].text)

else:
    print(f"Choix invalide : {choice!r}")
