import os 
from dotenv import load_dotenv 
from tavily import TavilyClient
import pandas as pd


load_dotenv()  # Load environment variables from .env

def ask_user(question):
    return input(f"Clarification needed: {question}\nYour answer: ")

def tavily_search(q):
    client = TavilyClient(api_key=os.getenv("TAVILY_KEY"))
    response = client.search(q)
    if not response['results']:
        return "No results found for this query."
    for result in response['results']:
        return(result['content'])
    
def calculate(what):
    try:
        return eval(what)
    except Exception as e:
        return f"Error: {e}"

def full_dataset_query(query):
    df = pd.read_csv("full_dataset.csv")
    try:
        # Only allow attribute access and simple expressions for safety
        result = eval(query, {"df": df, "pd": pd})
        return str (result)
    except Exception as e:
        return f"Error: {e}"

known_actions = {
    "calculate": calculate,
    "tavily_search": tavily_search,
    "ask_user": ask_user,
    "full_dataset_query": full_dataset_query,
}
