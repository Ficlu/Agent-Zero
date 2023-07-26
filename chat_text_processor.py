from chat_completion import ChatCompletion
class ChatTextProcessor:
    def __init__(self):
        pass
    #expects 
    #   string
    #outputs
    #   string
    def process(self, system_message, input):
        # Make openai request
        output = ChatCompletion.complete(self,[
        {"role": "system", "content": system_message},
        {"role": "user", "content": input}
        ],"gpt-4")
        return output