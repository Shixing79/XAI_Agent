import re
from chatbot import ChatBot
from actions import known_actions

class Agent:
  def __init__(self, system_prompt="", max_turns=1, known_actions=None):
    self.max_turns = max_turns
    self.bot = ChatBot(system_prompt)
    self.known_actions = known_actions
    self.action_re = re.compile('^Action: (\w+): (.*)')
    self.awaiting_user_input = False
    self.question_for_user = ""

  def run(self, question=None, user_response=None):
    if self.awaiting_user_input and user_response is not None:
        prompt = f"Observation: {user_response}"
        self.awaiting_user_input = False
        self.question_for_user = ""
    elif question is not None:
        prompt = question
    else:
        # Handle cases where we are not awaiting input and no question is provided
        return

    i=0
    while i < self.max_turns:
      i+=1
      result = self.bot(prompt)
      print(result)
      actions = [self.action_re.match(a) for a in result.split('\n') if self.action_re.match(a)]
      if actions:
        action, action_input = actions[0].groups()
        if action not in self.known_actions:
          raise Exception(f"Unknown action: {action} for action input: {action_input}")
        print(f"-- Running action: {action} {action_input}")

        if action == "ask_user":
            self.awaiting_user_input = True
            self.question_for_user = self.known_actions[action](action_input)
            print(f"--- QUESTION FOR USER: {self.question_for_user}")
            return # Stop processing and wait for user input
        else:
            observation = self.known_actions[action](action_input)
            print(f"-- Observation: {observation}")
            prompt = f"Observation: {observation}"
      else:
        return