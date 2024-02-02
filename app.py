from flask import Flask
from faultpilot_sdk import BackgroundLogger

app = Flask(__name__)

# Configure the BackgroundLogger within app.py
server_url = 'http://127.0.0.1:8090/error_tracker/log_error/'
background_logger = BackgroundLogger(app)
background_logger.set_server_url(server_url)
background_logger.set_api_key('Bi4BGlw-PjrB2eLCxtcMErfH3AsRciAOOZNL5v6fIAA')  # Replace with the actual API key

@app.route('/')
def home():
    # Your normal route logic here
    # give me intentional error
    x = "10"
    y = 5
    Z = x + y
    print(z)

if __name__ == '__main__':
    app.run(debug=True)
