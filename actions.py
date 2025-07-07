import os
from dotenv import load_dotenv
import pandas as pd
import shap
import joblib
import re
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend suitable for scripts and servers
import matplotlib.pyplot as plt
from sklearn.inspection import partial_dependence
from sklearn.inspection import PartialDependenceDisplay
import json
from pathlib import Path

load_dotenv()

def ask_user(question):
    # Instead of input(), return a special marker for the frontend
    return {"ask_user": question}

def calculate(what):
    try:
        return eval(what)
    except Exception as e:
        return f"Error in calculate: {e}"

def full_dataset_query(query):
    try:
        df = pd.read_csv("full_dataset.csv")
        # Only allow attribute access and simple expressions for safety
        result = eval(query, {"df": df, "pd": pd})
        return str(result)
    except Exception as e:
        return f"Error in full_dataset_query: {e}"

def local_feature_importance(query):
    try:
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
    except Exception as e:
        return f"Error in explain_prediction: {e}"

def global_feature_importance(_=None):
    try:
        # Load model and validation data
        model = joblib.load("lgbm_model.joblib")
        df = joblib.load("X_valid.joblib")
        # Compute SHAP values
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(df)
        # Mean absolute SHAP value for each feature
        mean_abs_shap = abs(shap_values).mean(axis=0)
        feature_names = df.columns.tolist()
        importance_list = sorted(zip(feature_names, mean_abs_shap), key=lambda x: -x[1])
        result = "Global SHAP Feature Importances (mean |SHAP value|):\n"
        for name, imp in importance_list[:5]:
            result += f"  {name}: {imp:.4f}\n"
        return result
    except Exception as e:
        return f"Error in global_feature_importance: {e}"

def partial_dependence_plot(query):
    try:
        feature = query.strip()
        model = joblib.load("lgbm_model.joblib")
        df = joblib.load("X_valid.joblib")
        if feature not in df.columns:
            return f"Feature '{feature}' not found in dataset."
        # Convert integer columns to float for partial dependence
        if pd.api.types.is_integer_dtype(df[feature]):
            df[feature] = df[feature].astype(float)

        plt.figure()
        display = PartialDependenceDisplay.from_estimator(model, df, [feature])
        # Save to static/plots/
        os.makedirs("static/plots", exist_ok=True)
        filename = f"partial_dependence_{feature}.png"
        filepath = os.path.join("static/plots", filename)
        plt.savefig(filepath)
        plt.close('all')
        # Return a special marker for the frontend
        return {
            "image_url": f"/static/plots/{filename}",
            "message": f"Partial dependence plot for '{feature}':"
        }
    except Exception as e:
        return f"Error in partial_dependence_plot: {e}"

def feature_description(feature_name, metadata_path="metadata.md"):
    """
    Returns the description of a feature from the metadata file.
    """
    try:
        # Load metadata.json block from metadata.md
        with open(metadata_path, "r") as f:
            lines = f.readlines()
        # Find the JSON block in the markdown file
        start = next(i for i, line in enumerate(lines) if line.strip().startswith("{"))
        end = len(lines) - next(i for i, line in enumerate(reversed(lines)) if line.strip().endswith("}"))
        json_str = "".join(lines[start:end])
        metadata = json.loads(json_str)
        # Search for the feature
        for col in metadata["columns"]:
            if col["name"].lower() == feature_name.strip().lower():
                return f"{col['name']}: {col['description']}"
        return f"Feature '{feature_name}' not found in metadata."
    except Exception as e:
        return f"Error in feature_description: {e}"

def get_prediction(query):
    try:
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

        pred = model.predict(row)[0]
        return f"Prediction for model={model_name}, week={week}: {pred:.4f}"
    except Exception as e:
        return f"Error in get_prediction: {e}"

def generate_and_save_graph(query):
    """
    Generates a matplotlib graph based on the query using LLM, executes the code, and saves the graph.
    """
    try:
        # Use the LLM to generate Python code for the graph
        from chatbot import ChatBot
        llm = ChatBot(system="You are a Python code generator for matplotlib graphs. Only generate code that creates a matplotlib graph based on the user's query. Do not include any other text or explanations. Never create syntaic data. Use data from full_dataset.csv or X_valid.joblib if necessary. Model ID is stored in column 'model', Year is stored in 'Year', week is stored as 'WeekNum'. The forecast/target variable is 'uplifted_sell_out'.")
        code = llm(f"Generate Python code to create a matplotlib graph for: {query}")

        print("Generated Code:\n", code)

        # Extract the title from the code (fallback to a default title)
        title_match = re.search(r"plt\.title\s*\(\s*[\"'](.+?)[\"']\s*\)", code)
        title = title_match.group(1) if title_match else "graph"

        # Sanitize the title to create a valid filename
        sanitized_title = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")

        # Define a safe execution environment
        safe_globals = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "min": min,
                "max": max,
                "sum": sum,
                "__import__": __import__,  # Allow dynamic imports
            },
            "plt": plt,
            "pd": pd,
            "os": os,
        }
        safe_locals = {}

        # Execute the generated code
        exec(code, safe_globals, safe_locals)

        # Save the graph with a filename based on the title
        os.makedirs("static/plots", exist_ok=True)
        filename = f"{sanitized_title}.png"
        filepath = os.path.join("static/plots", filename)
        plt.savefig(filepath)
        plt.close('all')

        # Return the graph's URL
        return {
            "image_url": f"/static/plots/{filename}",
            "message": f"Graph '{title}' generated and saved successfully."
        }
    except Exception as e:
        return f"Error in generate_and_save_graph: {e}"

known_actions = {
    "calculate": calculate,
    "ask_user": ask_user,
    "full_dataset_query": full_dataset_query,
    "local_feature_importance": local_feature_importance,
    "global_feature_importance": global_feature_importance,
    "partial_dependence_plot": partial_dependence_plot,
    "feature_description": feature_description,
    "get_prediction": get_prediction,
    "generate_and_save_graph": generate_and_save_graph,
}
