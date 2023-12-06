import unittest
import json
from unittest.mock import patch, MagicMock
from my_logger import BackgroundLogger

class TestBackgroundLogger(unittest.TestCase):

    def setUp(self):
        self.app = MagicMock()
        self.logger = BackgroundLogger(self.app, log_file='test_logs.log')
        self.logger.set_server_url('http://127.0.0.1:8080/error_logger/log_error/')

    def test_send_error_to_server_success(self):
        with patch('requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response

            exception = ValueError('Test Error')
            self.logger.send_error_to_server(exception)

            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            self.assertEqual(kwargs['url'], 'http://127.0.0.1:8080/error_logger/log_error/')
            
            # Check that the payload is correctly formatted as JSON
            expected_payload = {
                'error_type': 'Server Error',
                'error_name': 'Test Error',
                'error_message': 'Test Error',
                'stack_trace': self.logger.get_stack_trace(exception),
                'url': None,  # Replace with the expected value based on your application
                'user_agent': None,  # Replace with the expected value based on your application
                'browser': None,  # Replace with the expected value based on your application
                'os': None,  # Replace with the expected value based on your application
                'breadcrumbs': '{}',  # Replace with the expected value based on your application
            }
            self.assertDictEqual(json.loads(kwargs['json']), expected_payload)

    def test_send_error_to_server_failure(self):
        with patch('requests.post') as mock_post:
            mock_post.side_effect = Exception('Test Connection Error')

            exception = ValueError('Test Error')
            self.logger.send_error_to_server(exception)

            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            self.assertEqual(kwargs['url'], 'http://127.0.0.1:8080/error_logger/log_error/')
            
            # Check that the payload is correctly formatted as JSON
            expected_payload = {
                'error_type': 'Server Error',
                'error_name': 'Test Error',
                'error_message': 'Test Error',
                'stack_trace': self.logger.get_stack_trace(exception),
                'url': None,  # Replace with the expected value based on your application
                'user_agent': None,  # Replace with the expected value based on your application
                'browser': None,  # Replace with the expected value based on your application
                'os': None,  # Replace with the expected value based on your application
                'breadcrumbs': '{}',  # Replace with the expected value based on your application
            }
            self.assertDictEqual(json.loads(kwargs['json']), expected_payload)

    def test_set_server_url(self):
        self.logger.set_server_url('http://new-server.com/')
        self.assertEqual(self.logger.server_url, 'http://new-server.com/')

    def test_init_app(self):
        app = MagicMock()
        self.logger.init_app(app)
        self.assertEqual(self.logger.app, app)

    def test_setup_logger(self):
        log_file = 'test_setup_logs.log'
        self.logger.setup_logger(log_file)
        self.assertEqual(self.logger.logger.handlers[0].baseFilename, log_file)

if __name__ == '__main__':
    unittest.main()
