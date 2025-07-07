import re
from chatbot import ChatBot
from actions import known_actions

class Agent:
    def __init__(self, system_prompt="", max_turns=10, known_actions=None):
        self.max_turns = max_turns
        self.bot = ChatBot(system_prompt)
        self.known_actions = known_actions
        self.action_re = re.compile(r'^Action: (\w+):?\s*(.*)')

    def extract_section(self, text, section):
        # Extracts everything after 'section:' up to the next section or end of text
        pattern = rf'{section}:(.*?)(?:\n(?:\w+:)|$)'
        m = re.search(pattern, text, re.DOTALL)
        if m:
            return m.group(1).strip()
        return ""

    def run(self, question):
        i = 0
        prompt = question
        last_thought = ""
        last_observation = ""
        while i < self.max_turns:
            i += 1
            result = self.bot(prompt)
            print(result)
            thought = self.extract_section(result, "Thought")
            last_thought = thought or last_thought
            actions = [self.action_re.match(a) for a in result.split('\n') if self.action_re.match(a)]
            if actions:
                action, action_input = actions[0].groups()
                if action not in self.known_actions:
                    raise Exception(f"Unknown action: {action} for action input: {action_input}")
                print(f"-- Running action: {action} {action_input}")
                observation = self.known_actions[action](action_input)
                print(f"Observation: {observation}")
                last_observation = observation if isinstance(observation, str) else ""
                # If ask_user, propagate to frontend
                if isinstance(observation, dict):
                    if "ask_user" in observation:
                        return observation
                    if "image_url" in observation:
                        return observation
                prompt = f"Observation: {observation}"
            else:
                answer = self.extract_section(result, "Answer")
                # If not found, fallback to the whole result
                if not answer:
                    answer = result
                return {
                    "thought": last_thought,
                    "observation": last_observation,
                    "response": answer
                }
        return {
            "thought": last_thought,
            "observation": last_observation,
            "response": result
        }
