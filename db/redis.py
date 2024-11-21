from flask_redis import FlaskRedis

class Redis:
    """Redis Connection with Flask integration."""

    def __init__(self, app=None):
        self.redis = FlaskRedis()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the connection with a Flask app."""
        self.redis.init_app(app)

    def get_redis(self):
        """Get the Redis instance."""
        return self.redis

    def set(self, key, value):
        """Set a value in Redis."""
        self.redis.set(key, value)

    def get(self, key):
        """Get a value from Redis."""
        return self.redis.get(key)

    def delete(self, key):
        """Delete a value from Redis."""
        return self.redis.delete(key)

