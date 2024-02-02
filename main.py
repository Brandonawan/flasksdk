from flask import Flask
from faultpilot_sdk import BackgroundLogger
from loggy import ErrorTrackerSDK

app = Flask(__name__)

server_url = 'Bi4BGlw-PjrB2eLCxtcMErfH3AsRciAOOZNL5v6fIAA'
api_key = 'http://127.0.0.1:8090/error_tracker/log_error/'

error_tracker = ErrorTrackerSDK(server_url, api_key)
error_tracker.init_app(app)  # Initialize the app instance

@app.route('/')
def index():
    # Simulate an error
    1 / 0

if __name__ == "__main__":
    app.run(debug=True)
