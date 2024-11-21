
from loggers.base_logger import BaseLogger
from decorators.log_websocket_decorator import log_websocket_decorator
from functools import wraps
from datetime import datetime

class ConnectionLogger(BaseLogger):
    def __init__(self):
        super().__init__('connection_logger')

    def log_connection_status(self, user_info, status):
        self.logger.info(f'User: {user_info}, Connection status: {status}')

    @log_websocket_decorator
    def log_websocket_connection(self, user_info, status):
        """
        Decorator to log each WebSocket connection and disconnection with user info and timestamp.
        """
        print(f"User info: {user_info}, Status: {status}")
