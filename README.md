# Forecast Genie (XAI_Agent)

**Forecast Genie** is an interactive, explainable AI agent for demand forecasting, inventory management, and sales analysis. Users can query a machine learning model and its dataset using natural language, receiving clear, business-focused explanations for predictions and data insights.

## Features

- **Conversational Interface:** Chat with the agent about sales, inventory, forecasts, and model results via web.
- **ML Explainability:** View local and global feature importance, grouped into business categories, with plain-language impact explanations.
- **Data Explainability:** Run Python/pandas queries on the underlying dataset.
- **Visualization:** Generate and view plots for ML explainability and Data Explainability.
- **Business Context:** All answers are tailored for business stakeholders, avoiding technical jargon.

## Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your OpenAI API key:**
   - Create a `.env` file and add your API key as `XAI_KEY=...`


3. **Run the web app:**
   ```bash
   python app.py
   ```
   - The app will start a local web server. Open your browser to `http://localhost:5001`.

5. **Interact:**
   - Type your question in the chat box.

## Example Questions

- "Which features are most important for the model?"
- "Why did the model predict high sales for model 488QGLEC in week 202513?"
- "Show me the average raw stock on hand."
- "What does the feature `13w_sellout` mean?"
- "Plot the partial dependence of `rawsoh`."
- "How did sales change from last year to this year for model 271CCVNB?"

## Project Structure

- `main.py` — Entry point for the terminal agent (Alternative to Web)
- `app.py` — Web app entry point.
- `agent.py` — Core agent logic.
- `actions.py` — Implements available actions (feature importance, plotting, etc.).
- `chatbot.py` — Chat interface logic.
- `system_prompt.txt` — System prompt and action definitions.
- `full_dataset.csv` — Main dataset (**not included for confidentiality reasons**).
- `X_valid.joblib` — Validation set for the model (**not included for confidentiality reasons**).
- `metadata.md` — Dataset and feature descriptions (**not included for confidentiality reasons**).
- `requirements.txt` — Python dependencies.
- `static/` — Frontend assets (JS, CSS, plots).
- `templates/` — HTML templates.

## Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies.

## Notes

- The agent uses OpenAI API; set up your API keys as described above.
- The dataset file (`full_dataset.csv`), (`X_valid.joblib`) (`metadata.md`) are required for data queries and model predictions, but are **not included in this repository for confidentiality reasons**.
- Generated plots are saved in `static/plots/` and displayed in the chat when relevant.