
from config import client, APP_CLIENT_ID
import logging
from flask import Blueprint, request, jsonify, session, current_app
user_bp = Blueprint('user', __name__)

@user_bp.route('/sign-in', methods=['POST'])
def sign_in():
    data = request.get_json()
    print(data)
    username = data.get('username')
    password = data.get('password')

    try:
        response = current_app.client.initiate_auth(
            ClientId=current_app.APP_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            }
        )
        session['username'] = username
        
        return jsonify({'message': 'Sign in successful'}), 200

    except client.exceptions.NotAuthorizedException:
        return jsonify({'message': 'Incorrect username or password'}), 400
    except Exception as e:
        print(f"Exception during sign-in: {e}")  
        return jsonify({'message': 'Sign in failed.', 'error': str(e)}), 400


@user_bp.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)
    email = data.get('email', None)
    given_name = data.get('given_name', None)
    birthdate = data.get('birthdate', None)

    if not all([username, password, email, given_name, birthdate]):
        return jsonify({'message': 'Missing parameters'}), 400

    try:
        response = client.sign_up(
            ClientId=APP_CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name':'given_name',
                    'Value':given_name
                },
                {
                    'Name':'birthdate',
                    'Value':birthdate
                }
            ]
        )
        logging.info(f'Sign up response from AWS: {response}')
        session['username'] = username
        return jsonify({'message': 'Sign up successful'}), 200  
    except client.exceptions.UsernameExistsException:
        return jsonify({'message': 'User already exists'}), 400
    except Exception as e:
        logging.error(f'Sign up error: {e}')
        return jsonify({'message': 'Sign up failed.', 'error': str(e)}), 400

@user_bp.route('/confirm-sign-up', methods=['POST'])
def confirm_sign_up():
    data = request.get_json()
    print(data)
    username = data.get('username')
    confirmCode = data.get('confirmCode')

    try:
        response = client.confirm_sign_up(
            ClientId=APP_CLIENT_ID,
            Username=username,
            ConfirmationCode=confirmCode,
        )
        session['username'] = username
        return jsonify({'message': 'Confirmation successful'}), 200  
    except client.exceptions.CodeMismatchException:
        return jsonify({'message': 'Invalid confirmation code'}), 400
    except Exception as e:
        return jsonify({'message': 'Confirmation failed.', 'error': str(e)}), 400
