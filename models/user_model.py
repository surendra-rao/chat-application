import os
import random
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image, ImageDraw
from models.base_model import BaseModel
from exceptions import UserNotFoundException
from exceptions import DatabaseConnectionException

class UserModel(BaseModel):
    """
    User model to manage user registration, authentication, and avatar generation.
    """

    def __init__(self, username, password, email, mongo_db):
        """Initialize a user with a username, password, and email."""
        super().__init__(mongo_db)  
        self.username = username
        self.password_hash = generate_password_hash(password)  # Hash the password
        self.password = password
        self.email = email
        self.avatar = self.generate_random_avatar()  # Generate random avatar
        self.created_at = datetime.now(timezone.utc)
        self.last_active_at = datetime.now(timezone.utc)

    def generate_random_avatar(self):
        """Generate a random avatar and save it as a PNG file."""
        avatar_size = (100, 100)
        avatar = Image.new('RGB', avatar_size, (255, 255, 255))  # White background
        draw = ImageDraw.Draw(avatar)

        for _ in range(10):
            shape_color = tuple(random.randint(0, 255) for _ in range(3))
            x0, x1 = sorted([random.randint(0, 100) for _ in range(2)])
            y0, y1 = sorted([random.randint(0, 100) for _ in range(2)])
            draw.rectangle([x0, y0, x1, y1], fill=shape_color)

        avatar_dir = 'static/avatars'
        if not os.path.exists(avatar_dir):
            os.makedirs(avatar_dir)

        avatar_path = os.path.join(avatar_dir, f'{self.username}.png')
        avatar.save(avatar_path)

        return avatar_path

    @staticmethod
    def find_user(username, mongo_db):
        """Find a user by username in the database."""
        try:
            user = BaseModel(mongo_db).find_one('users', {'username': username})
            if user is None:
                raise UserNotFoundException(username)  # Raise custom exception if user not found
            return user
        
        except ConnectionError:  # Catch specific database connection errors
            raise DatabaseConnectionException("MongoDB")

    def save_to_db(self):
        """Save the user object to the database."""
        data = {
            'username': self.username,
            'password_hash': self.password_hash,
            'email': self.email,
            'avatar': self.avatar,
            'created_at': self.created_at,
            'last_active_at': self.last_active_at
        }
        try:
            super().save_to_db('users', data)
        except ConnectionError:
            raise DatabaseConnectionException("MongoDB")

    def verify_password(self, password):
        """Verify the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def update_last_active(self):
        """Update the last active timestamp for the user."""
        self.last_active_at = datetime.now(timezone.utc)
        try:
            super().update_in_db('users', {'username': self.username}, {'last_active_at': self.last_active_at})
        except ConnectionError:
            raise DatabaseConnectionException("MongoDB")

    def update_user(self, update_data):
        """Update user information in the database."""
        try:
            super().update_in_db('users', {'username': self.username}, update_data)
        except ConnectionError:
            raise DatabaseConnectionException("MongoDB")
