from flask import Flask, request, jsonify, render_template
from agent import Agent
from actions import known_actions

app = Flask(__name__, static_folder="static", template_folder="templates")

# Initialize the agent
def create_agent():
    return Agent(
        system_prompt=open("system_prompt.txt", "r").read(),
        max_turns=5,
        known_actions=known_actions
    )

agent = create_agent()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset():
    global agent
    agent = create_agent()
    return jsonify({"status": "reset"})

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "").strip()
    if user_question.lower() in ['q', 'quit', 'exit']:
        return jsonify({"response": "Goodbye!"})
    try:
        agent_response = agent.run(user_question)
        if isinstance(agent_response, dict):
            if "ask_user" in agent_response:
                return jsonify({"clarification": agent_response["ask_user"]})
            if "image_url" in agent_response:  # Handle graph responses
                return jsonify({
                    "image_url": agent_response["image_url"],
                    "message": agent_response.get("message", "")
                })
            # New: Return thought, observation, response
            return jsonify({
                "thought": agent_response.get("thought", ""),
                "observation": agent_response.get("observation", ""),
                "response": agent_response.get("response", "")
            })
        return jsonify({"response": agent_response})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)