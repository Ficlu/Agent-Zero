from flask import Blueprint, render_template, redirect, url_for, session, jsonify
from config import app
from memory_controller import MemoryController
import boto3
from botocore.exceptions import BotoCoreError, ClientError

page_requests = Blueprint('page_requests', __name__)

@page_requests.route('/')
def landing():
    return render_template('landing.html')

@page_requests.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('page_requests.landing'))

    return render_template('index.html')

@page_requests.route('/sign-up')
def signup_page():
    return render_template('signup.html')

@page_requests.route('/sign-in')
def signin_page():
    return render_template('signin.html')


@page_requests.route('/load_vars')
def load_vars():
    username = session.get('username', None)
    if not username:
        return jsonify(error="User not logged in"), 401  
    
    agents_chat_ids = MemoryController.load_agent_chat_index(username) 
    import json
    print("hey ", json.dumps(agents_chat_ids))
    return jsonify(agents_chat_ids)

@page_requests.route('/logout')
def logout():
    try:
        session.pop('username', None)
        return redirect(url_for('page_requests.landing'))
    except (BotoCoreError, ClientError) as error:
        return jsonify({'error': str(error)}), 400


@page_requests.route('/profile')
def profile():
    username = session.get('username', None)
    if not username:
        return redirect(url_for('page_requests.landing'))
    return render_template('user_profile.html')