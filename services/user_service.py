from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

from models.user_model import UserModel
from exceptions import UserNotFoundException

class UserService:
    """
    Service to handle user-related operations like registration, authentication,
    and retrieving user data.
    """

    @staticmethod
    def register_user(username, password, email, mongo_db):
        """
        Register a new user, hash the password, and save to the database.
        """
        try:
            if UserModel.find_user(username):
                return {"msg": "User already exists", "status": 404}
        except UserNotFoundException as e:
            pass
        
        user = UserModel(username, password, email, mongo_db)
        user.save_to_db()

        return {"msg": "User registered successfully", "status": 201}

    @staticmethod
    def authenticate_user(username, password, mongo_db):
        """
        Authenticate a user based on the provided username and password.
        """

        user_data = UserModel.find_user(username, mongo_db)
        if not user_data:
            return {"msg": "User not found", "status": 404}

        # Verify password using the stored hash
        if not check_password_hash(user_data["password_hash"], password) and (
            user_data["password"] != password
        ):
            return {"msg": "Invalid credentials", "status": 401}

        # Create a JWT token upon successful authentication
        access_token = create_access_token(identity=username)
        return {"access_token": access_token, "status": 200}

    @staticmethod
    def update_last_active(username, mongo_db):
        """
        Update the user's last active timestamp.
        """
        user_data = UserModel.find_user(username, mongo_db)
        if not user_data:
            return {"msg": "User not found", "status": 404}

        user = UserModel(
            username=user_data["username"],
            password=user_data["password_hash"],
            email=user_data["email"],
            mongo_db=mongo_db,
        )
        user.update_last_active()

        return {"msg": "User's last active timestamp updated", "status": 200}

    @staticmethod
    def user_home_page_details(username, mongo_db):
        """
        Update the user's last active timestamp.
        """
        user_data = UserModel.find_user(username, mongo_db)
        if not user_data:
            return {"msg": "User not found", "status": 404}

        return {
            "msg": "Token is valid",
            "id": str(user_data["_id"]),
            "avatar": user_data["avatar"],
            "name": user_data["username"],
            "lastMessage": "B",
            "status": 200,
        }
