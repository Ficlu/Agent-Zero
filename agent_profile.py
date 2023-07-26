import boto3
from botocore.exceptions import BotoCoreError, ClientError
import random
class AgentProfile:
    @staticmethod
    def load(uname, agent_id):
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')  # Specify your region
        table = dynamodb.Table('agent_table')  # Replace with your table name

        try:
            response = table.get_item(
                Key={
                    'uname': uname,
                    'agent_id': agent_id
                }
            )
            # If there's no item matching the provided keys, get_item will not throw an error.
            # Instead, there will be no 'Item' key in the response. We handle this case below.
            if 'Item' not in response:
                print("No item found with the provided keys")
                return None
            else:
                return response['Item']
        except (BotoCoreError, ClientError) as error:
            print(error)
            raise Exception("Unable to load from DynamoDB")  # Raise an exception to be caught by the calling function
        
    def __init__(self, user_id, agent_name, agent_voice, agent_details):
        self.user_id = user_id
        self.agent_name = agent_name
        self.agent_details = agent_details
        self.agent_voice = agent_voice
        self.agent_id = random.randint(10**7, 10**8 - 1)
        self.dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')  # Specify your region
        self.table = self.dynamodb.Table('agent_table')  # Replace with your table name

    def save(self):
        try:
            print("save entered!")

            item = {
                'uname': self.user_id,  # this line is added
                'agent_id': self.agent_id,
                'user_id': self.user_id,
                'agent_name': self.agent_name,
                'agent_details': self.agent_details,
                'agent_voice': self.agent_voice
            }

            # print each item and its type


            response = self.table.put_item(Item=item)
            return self. agent_id

        except (BotoCoreError, ClientError) as error:
            print("Error " + error)
            raise Exception("Unable to save to dynamoDB")  # Raise an exception to be caught by the calling function
            

