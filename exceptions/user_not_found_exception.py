class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the database."""
    def __init__(self, user_id, message="User not found"):
        self.user_id = user_id
        super().__init__(f"{message}: {user_id}")