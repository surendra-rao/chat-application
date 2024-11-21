"""
Configuration settings for the Flask application.

Loads environment variables for MongoDB, JWT secret key, and Redis connection
from a .env file using python-dotenv.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Holds configuration variables for the app."""
    MONGO_URI = os.getenv('MONGO_URI')  # MongoDB connection string
    SECRET_KEY = os.getenv('SECRET_KEY')  # JWT secret key
    REDIS_URL = os.getenv('REDIS_URL')  # Redis connection URL
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
