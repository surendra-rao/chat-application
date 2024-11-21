from datetime import datetime

from flask import current_app, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_jwt_extended import jwt_required, get_jwt_identity

from decorators.authenticate_decorator import authenticate_decorator
from decorators.log_websocket_decorator import log_websocket_decorator
from error_handlers import ErrorHandler
from loggers.connection_logger import ConnectionLogger
from loggers.message_logger import MessageLogger
from models.message_model import MessageModel


class SocketService:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.users: dict = {}
        self.connection_logger = ConnectionLogger()
        self.message_logger = MessageLogger()

    def init_socket_handlers(self):
        @self.socketio.on("test_message")
        def handle_test_message(msg):
            """Handle a test message."""
            self.message_logger.log_message_sent("Test User", msg)
            emit("response", {"message": "Message received!"})

        @self.socketio.on("connect")
        @authenticate_decorator
        @log_websocket_decorator
        def handle_connect():
            """Handle user connection and broadcast a join message."""
            try:
                user = request.user
                status = "connected"
                self.connection_logger.log_connection_status(user, status)
                emit("message", f"{user} has joined the chat.", broadcast=True)
            except Exception as error:
                self.connection_logger.error(f"Error during connection: {error}")
                return ErrorHandler.handle_generic_error(error)

        @self.socketio.on("disconnect")
        @log_websocket_decorator
        def handle_disconnect():
            """Handle user disconnection."""
            try:
                user = request.user
                self.connection_logger.log_connection_status(user, "disconnected")
                print("User disconnected")
            except Exception as error:
                self.connection_logger.error(f"Error during disconnection: {error}")
                return ErrorHandler.handle_generic_error(error)

        @self.socketio.on("send_message")
        @log_websocket_decorator
        def handle_send_message(data):
            """Broadcast a message to all users."""
            try:
                room = data.get("room")
                message_text = data.get("message")
                username = data.get("username")
                message_data = {
                    "username": username,
                    "room_id": room,
                    "message": message_text,
                    "timestamp": datetime.utcnow(),
                }
                print(message_data)
                message = MessageModel(current_app.mongo_db)
                message.save_message(message_data)

                emit(
                    "receive_message",
                    {"message": message_text, "username": username},
                    room=room,
                )
            except Exception as error:
                self.message_logger.error(f"Error while sending message: {error}")
                return ErrorHandler.handle_generic_error(error)

        @self.socketio.on("join")
        @authenticate_decorator
        @log_websocket_decorator
        def on_join(data):
            """Handle a user joining a room."""
            try:
                username = request.user
                room = data["room"]
                join_room(room)
                self.users[username] = room
                emit(
                    "join_announcement",
                    {"message": f"{username} has joined the room."},
                    room=room,
                )
            except Exception as error:
                self.connection_logger.error(f"Error during room join: {error}")
                return ErrorHandler.handle_generic_error(error)

        @self.socketio.on("leave")
        @log_websocket_decorator
        def on_leave(data):
            """Handle a user leaving a room."""
            try:
                room = data["room"]
                username = request.user
                leave_room(room)
                self.users.pop(username, None)
                emit(
                    "leave_announcement",
                    {"message": f"{username} has left the room."},
                    room=room,
                )
            except Exception as error:
                self.connection_logger.error(f"Error during room leave: {error}")
                return ErrorHandler.handle_generic_error(error)

        @self.socketio.on("private_message")
        @log_websocket_decorator
        def handle_private_message(data):
            """Send a private message to a specific room."""
            try:
                username = request.user
                room = data["room"]
                message = data["message"]
                emit(
                    "receive_message", {"user": username, "message": message}, room=room
                )
            except Exception as error:
                self.connection_logger.error(f"Error during private message: {error}")
                return ErrorHandler.handle_generic_error(error)

        @self.socketio.on("send_notification")
        @log_websocket_decorator
        def send_notification(data):
            """Broadcast a notification to all users."""
            try:
                message = data["message"]
                emit("notification", message, broadcast=True)
            except Exception as error:
                self.connection_logger.error(f"Error during send notification: {error}")
                return ErrorHandler.handle_generic_error(error)
