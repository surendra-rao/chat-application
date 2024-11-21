import unittest
from unittest.mock import MagicMock
from models.message_model import MessageModel
from exceptions import  InvalidRoomException


class TestMessageModel(unittest.TestCase):
    """Test case class for the MessageModel class."""

    def setUp(self):
        """Set up the test environment by mocking the MongoDB connection."""
        self.mock_mongo_db = MagicMock()
        self.message_model = MessageModel(self.mock_mongo_db)
        setattr(self.message_model, 'mongo_db', self.mock_mongo_db)

    def test_save_message(self):
        """Test case for saving a message successfully."""
        message_data = {
            'room_id': '507f1f77bcf86cd799439011',
            'user_id': 'user1',
            'message': 'Hello, world!',
            'timestamp': '2024-11-14T12:34:56'
        }
        self.message_model.save_to_db = MagicMock(return_value=None)  # Simulate success

        self.message_model.save_message(message_data)

        self.mock_mongo_db['messages'].insert_one.assert_called_once_with(message_data)

    def test_get_messages(self):
        """Test case for retrieving messages successfully by room ID."""
        room_id = '507f1f77bcf86cd799439011'
        mock_messages = [
            {'room_id': room_id, 'user_id': 'user1', 'message': 'Hello', 'timestamp': '2024-11-14T12:34:56'},
            {'room_id': room_id, 'user_id': 'user2', 'message': 'Hi', 'timestamp': '2024-11-14T12:35:56'}
        ]

        self.mock_mongo_db.messages.find.return_value.sort.return_value = mock_messages

        result = self.message_model.get_messages(room_id)

        self.assertEqual(result, mock_messages)

    def test_get_messages_no_messages(self):
        """Test case for retrieving messages when no messages are found in a room."""
        room_id = '507f1f77bcf86cd799439011'

        self.mock_mongo_db.messages.find.return_value.sort.return_value = []

        with self.assertRaises(InvalidRoomException):
            self.message_model.get_messages(room_id)

    def tearDown(self):
        """Clean up any necessary resources after each test."""
        # Any necessary clean-up can be done here (e.g., resetting mock data)
        pass