
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.chat_service import ChatService
from error_handlers import ErrorHandler
from exceptions.database_connection_exception import DatabaseConnectionException
from exceptions.invalid_room_exception import InvalidRoomException
from loggers.message_logger import MessageLogger  

chat_blueprint = Blueprint('chat_blueprint', __name__)

# Initialize loggers
message_logger = MessageLogger()

# Error handler for chat-related exceptions
@chat_blueprint.errorhandler(Exception)
def handle_chat_exception(error):
    """Handle exceptions in chat routes."""
    message_logger.error(f"Chat exception: {error}")
    return ErrorHandler.handle_generic_error(error)

@chat_blueprint.route('/send_message', methods=['POST'])
def send_message():
    """
    Endpoint to send a message to a chat room.
    Expects JSON payload with 'username', 'room_id', and 'message'.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        room_id = data.get('room_id')
        message = data.get('message')

        # Validate input data
        if not username or not room_id or not message:
            raise ValueError("Invalid input data")

        response = ChatService.send_message(username, room_id, message, current_app.mongo_db)
        return jsonify(response), response.get('status', 200)
    
    except DatabaseConnectionException as ve: 
        message_logger.error(f"Exception For Database Connection  : {ve} ")
        return handle_chat_exception(ve)
    
    except ValueError as ve:
        message_logger.error(f"ValueError: {ve}")
        return ErrorHandler.handle_invalid_input(ve)
    
    except Exception as e:
        message_logger.error(f"Exception in send_message: {e}")
        return handle_chat_exception(e)

@chat_blueprint.route('/chat_history/<room_id>', methods=['GET'])
@jwt_required()
def chat_history(room_id):
    """
    Endpoint to retrieve chat history for a specific room.
    """
    try:
        if not room_id:
            raise ValueError("room_id should not empty")
        current_user = get_jwt_identity()

        page_size = int(request.args.get("page_size", 50))  
        page_num = int(request.args.get("page_num", 1)) 
        
        chat_history_generator = ChatService.get_chat_history(room_id, current_user, current_app.mongo_db, page_size, page_num)

        chat_history = [message for message in chat_history_generator]
        return jsonify(chat_history), 200
    
    except DatabaseConnectionException as ve: 
        message_logger.error(f"Exception For Database Connection  : {ve} ")
        return handle_chat_exception(ve)
    
    except InvalidRoomException as ve:
        message_logger.error(f"Exception Invali Room : {ve} ")
        return ErrorHandler.handle_invalid_input(ve)
    
    except ValueError as ve:
        message_logger.error(f"ValueError: {ve}")
        return ErrorHandler.handle_invalid_input(ve)
    
    except Exception as e:
        message_logger.error(f"Exception in chat_history: {e}")
        return handle_chat_exception(e)


