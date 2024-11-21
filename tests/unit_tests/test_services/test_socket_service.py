# import unittest
# from unittest.mock import MagicMock, patch
# from flask import Flask
# from flask_socketio import SocketIO
# from services.socket_service import SocketService


# class TestSocketService(unittest.TestCase):

#     def setUp(self):
#         # Set up Flask app and push application context
#         self.app = Flask(__name__)
#         self.app_context = self.app.app_context()
#         self.app_context.push()
        
#         # Initialize SocketIO and SocketService
#         self.mock_socketio = MagicMock(spec=SocketIO)
#         self.socket_service = SocketService(self.mock_socketio)
#         self.socket_service.init_socket_handlers()

#     def tearDown(self):
#         # Pop the application context after each test
#         self.app_context.pop()

#     @patch('services.socket_service.request', create=True)
#     @patch('services.socket_service.authenticate_decorator', lambda func: func)  # Skip decorator in test
#     @patch('services.socket_service.ConnectionLogger')
#     def test_handle_connect(self, MockConnectionLogger, mock_request):
#         with self.app.test_request_context('/socket.io/'):
#             # Mock user and connection logger
#             mock_request.user = "test_user"
#             mock_logger_instance = MockConnectionLogger.return_value

#             # Simulate socket connect event
#             self.socket_service.socketio.emit = MagicMock()
#             self.mock_socketio.on_event("connect", MagicMock())()

#             # Check if connection status was logged
#             mock_logger_instance.log_connection_status.assert_called_once_with("test_user", "connected")
#             # Check if emit was called with the expected message
#             self.socket_service.socketio.emit.assert_called_with("message", "test_user has joined the chat.", broadcast=True)

# #     @patch('services.socket_service.request')
# #     @patch('services.socket_service.ConnectionLogger')
# #     def test_handle_disconnect(self, MockConnectionLogger, mock_request):
# #         # Mock the user and connection logger
# #         mock_request.user = "test_user"
# #         mock_logger_instance = MockConnectionLogger.return_value

# #         # Simulate socket disconnect event
# #         self.socket_service.socketio.emit = MagicMock()
# #         self.mock_socketio.on_event("disconnect", MagicMock())()

# #         # Check if disconnection status was logged
# #         mock_logger_instance.log_connection_status.assert_called_once_with("test_user", "disconnected")

# #     @patch('services.socket_service.MessageModel')
# #     @patch('services.socket_service.request')
# #     def test_handle_send_message(self, MockMessageModel, mock_request):
# #         # Mock user, message logger, and message model
# #         mock_request.user = "test_user"
# #         mock_message_instance = MockMessageModel.return_value
# #         message_data = {
# #             "room": "room1",
# #             "message": "Hello, room!",
# #             "username": "test_user"
# #         }

# #         # Simulate socket send_message event
# #         self.socket_service.socketio.emit = MagicMock()
# #         self.mock_socketio.on_event("send_message", MagicMock())(message_data)

# #         # Verify message was saved and emit was called
# #         mock_message_instance.save_message.assert_called_once()
# #         self.socket_service.socketio.emit.assert_called_with(
# #             "receive_message",
# #             {"message": "Hello, room!", "username": "test_user"},
# #             room="room1"
# #         )

# #     @patch('services.socket_service.request')
# #     def test_on_join(self, mock_request):
# #         # Mock user and room
# #         mock_request.user = "test_user"
# #         data = {"room": "test_room"}

# #         # Simulate socket join event
# #         self.socket_service.socketio.emit = MagicMock()
# #         self.socket_service.users = {}

# #         self.mock_socketio.on_event("join", MagicMock())(data)

# #         # Check if user is added to room and announcement is emitted
# #         self.assertIn("test_user", self.socket_service.users)
# #         self.assertEqual(self.socket_service.users["test_user"], "test_room")
# #         self.socket_service.socketio.emit.assert_called_with(
# #             "join_announcement",
# #             {"message": "test_user has joined the room."},
# #             room="test_room"
# #         )

# #     @patch('services.socket_service.request')
# #     def test_on_leave(self, mock_request):
# #         # Mock user and room
# #         mock_request.user = "test_user"
# #         data = {"room": "test_room"}
# #         self.socket_service.users = {"test_user": "test_room"}

# #         # Simulate socket leave event
# #         self.socket_service.socketio.emit = MagicMock()
# #         self.mock_socketio.on_event("leave", MagicMock())(data)

# #         # Check if user is removed from room and announcement is emitted
# #         self.assertNotIn("test_user", self.socket_service.users)
# #         self.socket_service.socketio.emit.assert_called_with(
# #             "leave_announcement",
# #             {"message": "test_user has left the room."},
# #             room="test_room"
# #         )

# #     @patch('services.socket_service.request')
# #     def test_handle_private_message(self, mock_request):
# #         # Mock user and room data for private message
# #         mock_request.user = "test_user"
# #         data = {"room": "room1", "message": "Hello privately!"}

# #         # Simulate private message event
# #         self.socket_service.socketio.emit = MagicMock()
# #         self.mock_socketio.on_event("private_message", MagicMock())(data)

# #         # Check if private message is emitted
# #         self.socket_service.socketio.emit.assert_called_with(
# #             "receive_message",
# #             {"user": "test_user", "message": "Hello privately!"},
# #             room="room1"
# #         )

# #     @patch('services.socket_service.request')
# #     def test_send_notification(self, mock_request):
# #         # Mock message data for notification
# #         data = {"message": "System Notification"}

# #         # Simulate send_notification event
# #         self.socket_service.socketio.emit = MagicMock()
# #         self.mock_socketio.on_event("send_notification", MagicMock())(data)

# #         # Check if notification is broadcasted to all users
# #         self.socket_service.socketio.emit.assert_called_with("notification", "System Notification", broadcast=True)


# # if __name__ == "__main__":
# #     unittest.main()
