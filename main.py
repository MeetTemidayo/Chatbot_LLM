import tkinter as tk
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# The LLM setup
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3.1")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    print("Welcome to the AI ChatbOT; Type 'exit' to quit. ")
    while True:
        user_input = input("You:  ")
        if user_input.lower() == "exit":
            break

        result = chain.invoke({"context": context, "question": user_input})
        print("Bot", result)
        context += f"\nUser: {user_input}\nAI: {result}" # for the Bot to know our previous converstaion


if __name__ == "__main__":
    handle_conversation()