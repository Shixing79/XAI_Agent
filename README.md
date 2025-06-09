# XAI_Agent

**XAI_Agent** is an interactive, explainable AI agent designed for demand forecasting, inventory management, and sales analysis. It enables users to query a machine learning model and its dataset using natural language, and provides transparent explanations for predictions using SHAP values and other interpretability tools.

## Features

- **Conversational Interface:** Ask questions about sales, inventory, model predictions, and more.
- **Explainable AI:** Get local and global feature importance using SHAP.
- **Data Exploration:** Query the underlying dataset with Python/pandas expressions.
- **Visualization:** Generate partial dependence plots for model features.
- **Web Search:** Retrieve external information using the Tavily API.
- **Clarification:** The agent can ask follow-up questions for ambiguous queries.

## Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the agent:**
   ```bash
   python main.py
   ```

3. **Interact:**
   - Type your question at the prompt.
   - Type `q`, `quit`, or `exit` to end the conversation.

## Example Questions

- "Which features are most important for the model?"
- "Why did the model predict high sales for model 488QGLEC in week 202513?"
- "Show me the average raw stock on hand."
- "What does the feature `13w_sellout` mean?"
- "Plot the partial dependence of `rawsoh`."

## Project Structure

- `main.py` — Entry point for the agent.
- `agent.py` — Core agent logic.
- `actions.py` — Implements available actions (feature importance, plotting, etc.).
- `system_prompt.txt` — System prompt and action definitions.
- `full_dataset.csv` — Main dataset (not included in repo).
- `metadata.md` — Dataset and feature descriptions.
- `requirements.txt` — Python dependencies.

## Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies.

## Notes

- The agent uses OpenAI and Tavily APIs; set up your API keys as needed.
- The dataset file (`full_dataset.csv`) is required for data queries and is not included in this repository.