class DatabaseConnectionException(Exception):
    """Exception raised for errors during database connection."""
    def __init__(self, db_name, message="Database connection failed"):
        self.db_name = db_name
        super().__init__(f"{message}: {db_name}")