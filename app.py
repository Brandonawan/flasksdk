from flask import Flask
from my_logger import BackgroundLogger

app = Flask(__name__)

# Configure the BackgroundLogger within app.py
server_url = 'http://127.0.0.1:8080/error_logger/log_error/'
background_logger = BackgroundLogger(app)
background_logger.set_server_url(server_url)

@app.route('/')
def home():
    # Your normal route logic here
    result = 1 / 0  # Intentional division by zero to trigger an error (replace with your actual code)
    return f'Result: {result}'

if __name__ == '__main__':
    app.run(debug=True)



# import sentry_sdk
# from flask import Flask
# from my_logger import BackgroundLogger

# app = Flask(__name__)

# # Initialize BackgroundLogger
# background_logger = BackgroundLogger(app)
# sentry_sdk.init(
#     dsn="https://0bbf1249f04175c23821d73ba7528cd5@o4506343604355072.ingest.sentry.io/4506348737134592",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     traces_sample_rate=1.0,
#     # Set profiles_sample_rate to 1.0 to profile 100%
#     # of sampled transactions.
#     # We recommend adjusting this value in production.
#     profiles_sample_rate=1.0,
# )

# @app.route('/')
# def home():
#     # Your normal route logic here
#     result = 1 / 0  # Intentional division by zero to trigger an error (replace with your actual code)
#     return f'Result: {result}'

# if __name__ == '__main__':
#     app.run(debug=True)


