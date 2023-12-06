import logging
from logging.handlers import RotatingFileHandler
from flask import request, g
import time
import requests
import json

class BackgroundLogger:
    def __init__(self, app=None, log_file='app_logs.log'):
        self.app = None
        self.server_url = None  # The server URL will be set from app.py
        self.setup_logger(log_file)
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.before_request(self.before_request)
        self.app.teardown_request(self.teardown_request)

    def set_server_url(self, server_url):
        self.server_url = server_url

    def setup_logger(self, log_file):
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

        handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
        handler.setLevel(logging.ERROR)  # Log only errors
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)  # Log only errors
        self.logger.addHandler(handler)

    def before_request(self):
        g.request_start_time = time.time()

    def teardown_request(self, exception):
        if exception and not request.path.startswith("/static"):
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            endpoint = request.endpoint
            method = request.method
            url = request.url
            elapsed_time = time.time() - g.request_start_time

            self.logger.error(f'Request details: IP={ip_address}, User-Agent={user_agent}, Endpoint={endpoint}, Method={method}, URL={url}')
            self.logger.exception(f'An error occurred:')

            # Send error data to the server
            self.send_error_to_server(exception)

    def send_error_to_server(self, exception):
        if not self.server_url:
            raise ValueError("Server URL is not set. Call set_server_url before using the logger.")

        error_data = {
            'error_type': 'Server Error',  # You might want to categorize errors based on the exception type
            'error_name': str(exception),
            'error_message': str(exception),
            'stack_trace': self.get_stack_trace(exception),
            'url': request.url,
            'user_agent': request.headers.get('User-Agent'),
            'browser': self.get_browser(request.headers.get('User-Agent')),
            'os': self.get_os(request.headers.get('User-Agent')),
            'breadcrumbs': '{}',  # You can customize this based on your application's breadcrumb data
        }

        try:
            response = requests.post(self.server_url, json=error_data)
            response.raise_for_status()
            self.logger.info(f'Successfully sent error data to the server.')
        except requests.RequestException as e:
            self.logger.warning(f'Failed to send error data to the server: {e}')

    def get_browser(self, user_agent):
        return user_agent.split()[0] if user_agent else 'Unknown Browser'

    def get_os(self, user_agent):
        return user_agent.split()[-1] if user_agent else 'Unknown OS'

    def get_stack_trace(self, exception):
        import traceback
        return traceback.format_exc()
