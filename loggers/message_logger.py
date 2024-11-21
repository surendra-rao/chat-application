
from loggers.base_logger import BaseLogger

class MessageLogger(BaseLogger):
    def __init__(self):
        super().__init__('message_logger')

    def log_message_sent(self, user_info, message):
        self.logger.info(f'User: {user_info}, Message sent: {message}')

    def log_message_received(self, user_info, message):
        self.logger.info(f'User: {user_info}, Message received: {message}')
