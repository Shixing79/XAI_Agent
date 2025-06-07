import httpx
import requests
import xml.etree.ElementTree as ET
import os 
from dotenv import load_dotenv 
from tavily import TavilyClient

ARXIV_NAMESPACE = '{http://www.w3.org/2005/Atom}'

load_dotenv()  # Load environment variables from .env

def ask_user(question):
    return input(f"Clarification needed: {question}\nYour answer: ")

def wikipedia(q):
    response = httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()
    if response["query"]["search"]:
        return response["query"]["search"][0]["snippet"]
    else:
        return "No Wikipedia article found for this query."

def arxiv_search(q):
    url = f'http://export.arxiv.org/api/query?search_query=all:{q}&start=0&max_results=1'
    res = requests.get(url)
    et_root = ET.fromstring(res.content)
    entries = et_root.findall(f"{ARXIV_NAMESPACE}entry")
    if not entries:
        return {"title": "No article found", "summary": "No summary available"}
    for entry in entries:
        title = entry.find(f"{ARXIV_NAMESPACE}title").text.strip()
        summary = entry.find(f"{ARXIV_NAMESPACE}summary").text.strip()
    return {"title": title, "summary": summary}

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


known_actions = {
    "wikipedia": wikipedia,
    "arxiv_search": arxiv_search,
    "calculate": calculate,
    "tavily_search": tavily_search,
    "ask_user": ask_user,
}
