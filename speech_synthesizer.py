from botocore.exceptions import ClientError
from system_messages.system_messages import SystemMessages
import boto3
from chat_completion import ChatCompletion
class SpeechSynthesizer:
    def __init__(self, region_name='ap-southeast-2'):
        self.polly_client = boto3.Session(region_name=region_name).client('polly')



    def synthesize_speech(self, text, voice):
        #text is the response in the SSML format
        print("here")
        ssml_text = self.format(text)  
        print(f"ssml_text: {ssml_text}")
        try:
            response = self.polly_client.synthesize_speech(
                VoiceId=voice,
                OutputFormat='mp3',
                Text=ssml_text,
                Engine='neural',
                TextType='ssml'
            )
        except ClientError as e:
            response = self.polly_client.synthesize_speech(
                VoiceId=voice,
                OutputFormat='mp3',
                Text=text,
                Engine='neural',
                TextType='text'
            )
            return response

        filename = 'static/speech.mp3'
        try:
            with open(filename, 'wb') as file:
                file.write(response['AudioStream'].read())
        except IOError as e:
            print(f"Error saving synthesized speech to file: {e}")
            return None

        return filename

    
    def format(self, message):
        system_message = SystemMessages.ssml_msg(self)
        print(system_message)
        prompt = [{'role': 'system', 'content': system_message}, 
                  {'role': 'user', 'content': message}]
        ssml_message = ChatCompletion.complete(self, prompt, 'gpt-4', 1.2)
        print('ssml_message: ' + ssml_message)
        return ssml_message

