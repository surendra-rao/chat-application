from functools import wraps
from datetime import datetime, timezone


def log_websocket_decorator(func):
        """
        Decorator to log each WebSocket connection and disconnection with user info and timestamp.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            instance = args[0] 
            user_info = kwargs.get('user_info') or 'Unknown User'
            status =  kwargs.get("status", "unknown")
            timestamp = datetime.now(timezone.utc)
            
            # Log the connection or disconnection
            instance.logger.info(f'{status.capitalize()} - User: {user_info}, Timestamp: {timestamp}')
            
            return func(*args, **kwargs)
        
        return wrapper