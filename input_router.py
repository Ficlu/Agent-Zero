from chat_text_processor import ChatTextProcessor
from memory_controller import MemoryController
from speech_synthesizer import SpeechSynthesizer
from system_messages.system_messages import SystemMessages

class InputRouter:
    def __init__(self):
        self.memory_controller = MemoryController()

    # expects 
    #   string
    # outputs
    #   string
    def route(self, user, agent_id, chat_id, message_id, datetime, input):
        # Load past messages from database
        
        past_messages = self.memory_controller.load_messages(user, agent_id, chat_id)
        system_message = SystemMessages.role_msg(self, user, agent_id)
        system_message += SystemMessages.chat_msg(self, user, agent_id)
        system_message += f"{past_messages}"
        print("system_message: " + system_message)

        # Get 'mid' from the most recent message
        mid = int(past_messages[0]['mid']) if past_messages else 0
        mid = mid+1
        print(f"{mid}")
        # Save the new user input
        self.memory_controller.save_user_input(user, agent_id, chat_id, mid, datetime, input)

        # Process the input and generate a response
        output = ChatTextProcessor().process(system_message, input)
        print(f"{output}")
        mid = mid+1
        self.memory_controller.save_agent_output(user, agent_id, chat_id, mid, datetime, output)
        voice = self.memory_controller.get_agent_voice(user, agent_id)
        name = self.memory_controller.get_agent_name(user, agent_id)
        # Convert the response to speech
        audio = SpeechSynthesizer().synthesize_speech(output, f'{voice}')

        # Print output for debugging and return the response and audio file
        return {"message": output, "aname": name, "speech_file": audio}
