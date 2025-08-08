import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('XAI_KEY')
client = OpenAI(api_key=api_key)

class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": self.system})

    def __call__(self, messsage):
        self.messages.append({"role": "user", "content": messsage})
        result = self.runllm()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def runllm(self):
        chat_completion = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=self.messages
        )
        return chat_completion.choices[0].message.content
