from flask import Flask
import boto3
import openai
import os
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)  # Change level to logging.DEBUG for more detailed output

# Cognito user pool info
USER_POOL_ID = [""] # use system variables for Amazon Cognito
APP_CLIENT_ID = [""] # use system variables for Amazon Cognito

client = boto3.client('cognito-idp', region_name='ap-southeast-2') # replace with your region_name
openai.api_key = os.getenv("OPENAI_API_KEY") #system var

app = Flask(__name__)
print("flask(__name__) created")
app.client = client  # attach the client object to the app instance
print("flask client attached")
app.APP_CLIENT_ID = APP_CLIENT_ID  # attach the APP_CLIENT_ID to the app instance
print("flask app id")
app.secret_key = 'yoursecretkey'
print("secret key")