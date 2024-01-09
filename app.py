# app.py
from flask import Flask
from my_logger import BackgroundLogger

app = Flask(__name__)

# Configure the BackgroundLogger within app.py
server_url = 'http://127.0.0.1:8080/error_tracker/log_error/'
background_logger = BackgroundLogger(app)
background_logger.set_server_url(server_url)
background_logger.set_api_key('1KUuD6vguT--9QveQpiV17xnSMFI1N7-XQslyi5JYRI')  # Replace with the actual API key

@app.route('/')
def home():
    # Your normal route logic here
    result = 1 / 0  # Intentional division by zero to trigger an error (replace with your actual code)
    return f'Result: {result}'

if __name__ == '__main__':
    app.run(debug=True)


