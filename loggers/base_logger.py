# loggers/base_logger.py
import logging
import logging.config
from loggers.logger_config import LOGGING_CONFIG

class BaseLogger:
    def __init__(self, logger_name):
        logging.config.dictConfig(LOGGING_CONFIG)
        self.logger = logging.getLogger(logger_name)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def log_user_action(self, user_info, action):
        self.logger.info(f'User: {user_info}, Action: {action}')
