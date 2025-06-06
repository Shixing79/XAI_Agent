import re
from chatbot import ChatBot
from actions import known_actions

class Agent:
  def __init__(self, system_prompt="", max_turns=1, known_actions=None):
    self.max_turns = max_turns
    self.bot = ChatBot(system_prompt)
    self.known_actions = known_actions
    self.action_re = re.compile('^Action: (\w+): (.*)')

  def run(self, question):
    i = 0
    prompt = question

    while i < self.max_turns:
      i += 1
      result = self.bot(prompt)
      print(result)
      actions = [self.action_re.match(a) for a in result.split('\n') if self.action_re.match(a)]
      if actions:
        action, action_input = actions[0].groups()
        if action not in self.known_actions:
          raise Exception(f"Unknown action: {action} for action input: {action_input}")
        print(f"-- Running action: {action} {action_input}")
        observation = self.known_actions[action](action_input)
        print(f"-- Observation: {observation}")
        prompt = f"Observation: {observation}"
      else:
        return
