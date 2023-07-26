from decimal import Decimal

#memory_controller.py
import boto3
from boto3.dynamodb.conditions import Key, Attr
import logging
from botocore.exceptions import ClientError
class MemoryController:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        self.message_table = self.dynamodb.Table('message_table')

    def save_user_input(self, user, agent_id, chat_id, message_id, datetime, input):
        self.message_table.put_item(
        Item={
                'chat_id': chat_id,
                'uname': user,
                'agent_id':  agent_id,
                'message_id': message_id,
                'message_date': datetime,
                'type':"input",
                'message_content': input
            }
        )
        logging.info(f"User input saved for chat_id {chat_id}")

    def save_agent_output(self, user, agent_id, chat_id, message_id, datetime, output):
        self.message_table.put_item(
        Item={
                'chat_id': chat_id,
                'uname': user,
                'agent_id':  agent_id,
                'message_id': message_id,
                'message_date': datetime,
                'type':"output",
                'message_content': output
            }
        )
        logging.info(f"Agent output saved for chat_id {chat_id}")

    def load_agent_chat_index(user):
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('agent_table')

        response = table.scan(
            FilterExpression=Attr('uname').eq(user)
        )

        agents = set()
        while True:   
            for item in response['Items']:
                agent_id = int(Decimal(item['agent_id']))

                agents.add((agent_id))

    
            if 'LastEvaluatedKey' not in response:
                break

            response = table.scan(
                FilterExpression=Attr('uname').eq(user),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )

        return list(agents)





    def load_messages(self, user, agent_id, chat_id):
        from boto3.dynamodb.conditions import Attr

        response = self.message_table.query(
            KeyConditionExpression=Key('chat_id').eq(chat_id),
            FilterExpression=Attr('uname').eq(user) & Attr('agent_id').eq(agent_id),
            Limit=4,
            ScanIndexForward=False
        )
        messages = response['Items']

        if not messages: 
            logging.info(f"No messages found for chat_id {chat_id}")
            return ""

        formatted_messages = [
            {"mid": message['message_id'], "dt": message['message_date'], f"{message.get('type')}": f"{message['message_content']}"}
            if index == 0
            else 
            {f"{message.get('type')}": f"{message['message_content']}"}
            for index, message in enumerate(messages)
        ]

        logging.info(f"Loaded messages for chat_id {chat_id}")
        return formatted_messages
    
    def get_agent_voice(self, user, agent_id):
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('agent_table')

        try:
            response = table.query(
                KeyConditionExpression=Key('uname').eq(user) & Key('agent_id').eq(agent_id)
            )

            if response['Count'] > 0:
                return response['Items'][0]['agent_voice']
            else:
                return "Agent not found"

        except ClientError as e:
            print(f"Error: {e}")
            return None
        
    def get_agent_name(self, user, agent_id):
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('agent_table')

        try:
            response = table.query(
                KeyConditionExpression=Key('uname').eq(user) & Key('agent_id').eq(agent_id)
            )

            if response['Count'] > 0:
                return response['Items'][0]['agent_name']
            else:
                return "Agent not found"
        except ClientError as e:
            print(f"Error: {e}")
            return None