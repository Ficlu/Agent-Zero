import boto3
from botocore.exceptions import BotoCoreError, ClientError

class UserProfile:
    @staticmethod
    def load(uname):
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')  # Specify your region
        table = dynamodb.Table('user_table')  # Replace with your table name

        try:
            response = table.get_item(
                Key={
                    'uname': uname

                }
            )
            if 'Item' not in response:
                print("No item found with the provided keys")
                return None
            else:
                return response['Item']
        except (BotoCoreError, ClientError) as error:
            print(error)
            raise Exception("Unable to load from DynamoDB")  # Raise an exception to be caught by the calling function
        
    def __init__(self, user_id, u_name, user_profile_details):
        self.user_id = user_id
        self.u_name = u_name
        self.user_profile_details = user_profile_details
        self.dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')  # Specify your region
        self.table = self.dynamodb.Table('user_table')  # Replace with your table name

    def save(self):
        try:
            print("save entered!")

            item = {
                'uname': self.user_id,  # this line is added
                'user_id': self.user_id,
                'u_name': self.u_name,
                'user_profile_details': self.user_profile_details
            }

            response = self.table.put_item(Item=item)
            return self.user_id

        except (BotoCoreError, ClientError) as error:
            print(f"Error{error}")
            raise Exception("Unable to save to DynamoDB")  # Raise an exception to be caught by the calling function
