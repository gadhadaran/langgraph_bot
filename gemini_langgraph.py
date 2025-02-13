!pip install langchain langgraph openai anthropic

!pip install -U langchain-community

import os
import google.generativeai as genai
import langgraph
from langgraph.graph import StateGraph

# Set your API key
GOOGLE_API_KEY = "AIzaSyBS1L2JanQLMbtK3tEYA-z5i0UW9beGMoA"
genai.configure(api_key=GOOGLE_API_KEY)

def query_google(state):
    """Queries Google Gemini API with the given prompt and returns the response."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(state["prompt"])
    output = response.text if response else "No response received."
    return {"response": output}

def chat_prompt():
    """Handles user input for interactive chat."""
    return input("You: ")

def autonomous_chat():
    """Runs an interactive chat with the AI agent using LangGraph."""
    graph = StateGraph(state_schema=dict)
    graph.add_node("query_google", query_google)
    graph.set_entry_point("query_google")
    agent = graph.compile()

    print("Start chatting with the AI. Type 'exit' to stop.")
    state = {"prompt": chat_prompt()}

    while state["prompt"].lower() != "exit":
        state = agent.invoke(state)
        print(f"Gemini: {state['response']}")
        state["prompt"] = chat_prompt()

    print("Chat session ended.")

if __name__ == "__main__":
    autonomous_chat()
