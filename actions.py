import os 
from dotenv import load_dotenv 
import pandas as pd
import shap
import joblib
import re
import matplotlib.pyplot as plt
from sklearn.inspection import partial_dependence
from sklearn.inspection import PartialDependenceDisplay
import json
from pathlib import Path

load_dotenv() 

def ask_user(question):
    try:
        return input(f"Clarification needed: {question}\nYour answer: ")
    except Exception as e:
        return f"Error in ask_user: {e}"

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
        filename = f"partial_dependence_{feature}.png"
        plt.savefig(filename)
        plt.close()
        return f"Partial dependence plot saved as '{filename}'."
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

def trend_of_uplifted_sell_out(query):
 
    try:
        df = pd.read_csv("full_dataset.csv")
        # Accept both "week" and "Numweek" in the query
        m = re.search(
            r'(year|week) on (year|week) trend.*model\s*([A-Za-z0-9]+).*(?:week|Numweek)\s*(\d+)(?:.*year\s*(\d+))?',
            query, re.IGNORECASE)
        if not m:
            return ("Please specify trend type, model, week, and optionally year. "
                    "E.g., 'year on year trend for model 488QGLEC week 13'")

        trend_type = m.group(1).lower()
        model = m.group(3)
        weeknum = int(m.group(4))
        year = int(m.group(5)) if m.group(5) else None

        if trend_type == "year":
            # Find all years for this model and weeknum
            rows = df[(df['model'] == model) & (df['WeekNum'] == weeknum)]
            if rows.shape[0] < 2:
                return (f"Not enough data for year-on-year trend for model={model}, week={weeknum}")
            # Sort by year and take last two years
            rows = rows.sort_values("Year")
            last2 = rows.iloc[-2:]
            y1, y2 = last2['Year'].values
            v1, v2 = last2['uplifted_sell_out'].values
            if v1 == 0:
                return ("Previous year's uplifted_sell_out is 0, cannot compute ratio.")
            ratio = v2 / v1
            return (f"Year-on-year trend for model={model}, week={weeknum}: "
                    f"{y1}={v1}, {y2}={v2}, ratio={ratio:.4f}")
        elif trend_type == "week":
            if not year:
                return "Please specify the year for week-on-week trend."
            # Find this week and previous week
            row = df[(df['model'] == model) & (df['WeekNum'] == weeknum) & (df['Year'] == year)]
            prev_row = df[(df['model'] == model) & (df['WeekNum'] == weeknum-1) & (df['Year'] == year)]
            if row.empty or prev_row.empty:
                return (f"Not enough data for week-on-week trend for model={model}, week={weeknum}, year={year}")
            v1 = prev_row.iloc[0]['uplifted_sell_out']
            v2 = row.iloc[0]['uplifted_sell_out']
            if v1 == 0:
                return ("Previous week's uplifted_sell_out is 0, cannot compute ratio.")
            ratio = v2 / v1
            return (f"Week-on-week trend for model={model}, year={year}, "
                    f"week {weeknum-1}={v1}, week {weeknum}={v2}, ratio={ratio:.4f}")
        else:
            return "Unknown trend type. Use 'year on year' or 'week on week'."
    except Exception as e:
        return f"Error in trend_of_uplifted_sell_out: {e}"

known_actions = {
    "calculate": calculate,
    "ask_user": ask_user,
    "full_dataset_query": full_dataset_query,
    "local_feature_importance": local_feature_importance,
    "global_feature_importance": global_feature_importance,
    "partial_dependence_plot": partial_dependence_plot,
    "feature_description": feature_description,
    "trend_of_uplifted_sell_out": trend_of_uplifted_sell_out,
}
