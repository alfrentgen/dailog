from llama_cpp import Llama
from abc import abstractmethod

class Model:
    @abstractmethod
    def process(self, message: str) -> str:
        pass

class Human(Model):
    def process(self, message: str) -> str:
        response = input('Human response: ')
        return response

class LLM(Model):
    def __init__(self, config: dict):
        self.model = Llama(**config)
        self.messages_history=[
            {
                'role': 'system',
                'content': config['prompt']
            },
        ]

    def add_user_message(self, message: str):
        self.messages_history.append(
            {
                'role': 'user',
                'content': message
            }
        )

    def get_message_from_response(self, response):
        return response['choices'][0]['message']['content']

    def process(self, message: str) -> str:
        self.add_user_message(message)
        response = self.model.create_chat_completion(
            messages=self.messages_history,
        )
        message = response['choices'][0]['message']['content']
        role = response['choices'][0]['message']['role']
        self.messages_history.append({'role': role, 'message': message})
        return self.get_message_from_response(response)
