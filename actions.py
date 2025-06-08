import os 
from dotenv import load_dotenv 
from tavily import TavilyClient
import pandas as pd
import shap
import joblib
import re


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

def explain_prediction(query):
    m = re.search(r"model\s*=?\s*([A-Za-z0-9]+)[,\s]+week\s*=?\s*([0-9]+)", query)
    if not m:
        return "Please specify model and week, e.g., model=488QGLEC,week=202513"
    model_name, week = m.group(1), m.group(2)

    # Load data and model
    df = joblib.load("X_valid.joblib")
    model = joblib.load("lgbm_model.joblib")

    # Find the row
    row = df[(df['model'] == model_name) & (df['week'] == int(week))]
    if row.empty:
        return f"No data found for model={model_name}, week={week}"

    # SHAP explanation
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(row)
    base_value = explainer.expected_value
    pred = model.predict(row)[0]

    # Get top features
    feature_cols = row.columns.tolist()
    top_idx = abs(shap_values[0]).argsort()[::-1][:5]
    top_features = [(feature_cols[i], shap_values[0][i]) for i in top_idx]

    # Format output
    explanation = f"Prediction for model={model_name}, week={week}: {pred:.4f}\n"
    explanation += f"Base value: {base_value:.4f}\n"
    explanation += "Top contributing features:\n"
    for feat, val in top_features:
        explanation += f"  {feat}: {val:.4f}\n"
    return explanation

known_actions = {
    "calculate": calculate,
    "tavily_search": tavily_search,
    "ask_user": ask_user,
    "full_dataset_query": full_dataset_query,
    "explain_prediction": explain_prediction,
}
