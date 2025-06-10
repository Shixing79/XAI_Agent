from agent import Agent
from actions import known_actions

if __name__ == "__main__":
    agent = Agent(system_prompt=open("system_prompt.txt", "r").read(), max_turns=5, known_actions=known_actions)
    print("What is your question for the agent?\nType 'q', 'quit' or 'exit' to end the conversation.")    
    while True:
        user_question = input("You: ")
        if user_question.strip().lower() in ['q', "quit", "exit"]:
            print("Goodbye!")
            break
        try:
            agent.run(user_question)
        except Exception as e:
            print(f"Sorry, something went wrong: {e}")