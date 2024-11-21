

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity

from exceptions import DatabaseConnectionException,UserNotFoundException
from services.user_service import UserService
# from db_connections.mongo_db_connection import MongoDB
from loggers.user_logger import UserLogger 
from error_handlers import ErrorHandler

user_blueprint = Blueprint('user_blueprint', __name__)

# Initialize loggers
user_logger = UserLogger()

# Error handler for user-related exceptions
@user_blueprint.errorhandler(Exception)
def handle_user_exception(error):
    """Handle exceptions in user routes."""
    user_logger.error(f"User exception: {error}") 
    return ErrorHandler.handle_generic_error(error)

@user_blueprint.route('/register', methods=['POST'])
def register():
    """
    Endpoint to register a new user.
    Expects JSON payload with 'username', 'password', and 'email'.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # Validate input data
        if not username or not password or not email:
             raise ValueError("Invalid input data")

        response = UserService.register_user(username, password, email, current_app.mongo_db)
        return jsonify(response), response.get('status', 201)  # 201 Created for successful registration

    except DatabaseConnectionException as e: 
        user_logger.error(f"Exception For Database Connection : {e} ")
        return handle_user_exception(e)
    
    except UserNotFoundException as e:
        user_logger.error(f"Exception User Not Found : {e} ")
        return handle_user_exception(e)
    
    except ValueError as ve:
        user_logger.error(f"ValueError during registration: {ve}")
        return ErrorHandler.handle_invalid_input(ve)
    
    except Exception as e:
        user_logger.error(f"Exception during registration: {e}")
        return handle_user_exception(e)

@user_blueprint.route('/login', methods=['POST'])
def login():
    """
    Endpoint to authenticate a user.
    Expects JSON payload with 'username' and 'password'.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # Validate input data
        if not username or not password:
            raise ValueError("Invalid input data")

        response = UserService.authenticate_user(username, password, current_app.mongo_db)
        return jsonify(response), response.get('status', 200)
    
    except DatabaseConnectionException as e: 
        user_logger.error(f"Exception For Database Connection : {e} ")
        return handle_user_exception(e)
    
    except UserNotFoundException as e:
        user_logger.error(f"Exception User Not Found : {e} ")
        return handle_user_exception(e)
    
    except ValueError as ve:
        user_logger.error(f"ValueError during login: {ve}")
        return ErrorHandler.handle_invalid_input(ve)

    except Exception as e:
        user_logger.error(f"Exception during login: {e}")
        return handle_user_exception(e)
    
@user_blueprint.route('/page_details', methods=['GET'])
@jwt_required()
def page_details():
    """Get current user details."""
    try:
        current_user = get_jwt_identity()
        response = UserService.user_home_page_details(current_user, current_app.mongo_db)
        return jsonify(response), response.get('status', 200)
    
    except DatabaseConnectionException as e: 
        user_logger.error(f"Exception For Database Connection  : {e} ")
        return handle_user_exception(e)
    
    except UserNotFoundException as e:
        user_logger.error(f"Exception User Not Found : {e} ")
        return handle_user_exception(e)
    except Exception as e:
        user_logger.error(f"Exception during page details : {e}")
        return handle_user_exception(e)
    
@user_blueprint.route('/static/avatars/<filename>')
def get_avatar(filename):
    """Serve user avatar."""
    return send_from_directory('avatars', filename)

