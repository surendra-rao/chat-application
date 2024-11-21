# loggers/user_logger.py
from loggers.base_logger import BaseLogger

class UserLogger(BaseLogger):
    def __init__(self):
        super().__init__('user_logger')

    def log_login(self, user_info):
        self.log_user_action(user_info, "logged in")

    def log_logout(self, user_info):
        self.log_user_action(user_info, "logged out")
