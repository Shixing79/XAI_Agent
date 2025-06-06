from agent import Agent
from actions import known_actions

if __name__ == "__main__":
    agent = Agent(system_prompt=open("prompt.txt", "r").read(), max_turns=5, known_actions=known_actions)
    user_question = input("What is your question for the agent? ")
    agent.run(user_question)