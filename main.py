from config import app
from flask import Flask
from user_management import user_bp
from process_requests import process_requests
from page_requests import page_requests

if __name__ == '__main__':
    print("Registering blueprints...")
    app.register_blueprint(user_bp)
    app.register_blueprint(process_requests)
    app.register_blueprint(page_requests)
    print("Blueprints registered.")


    app.run(host='0.0.0.0', port=5000, debug=True)
