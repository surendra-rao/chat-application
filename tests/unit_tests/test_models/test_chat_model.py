import unittest
from unittest.mock import MagicMock, patch
from models.chat_model import ChatModel
from bson.objectid import ObjectId

class TestChatModel(unittest.TestCase):
    """Test case class for the ChatModel class."""

    def setUp(self):
        """Set up the test environment by mocking the MongoDB connection."""
        self.mock_mongo_db = MagicMock()
        self.chat_model = ChatModel(self.mock_mongo_db)

    @patch.object(ChatModel, 'save_to_db')
    def test_save_chat_success(self, mock_save_to_db):
        """Test case for saving a chat session successfully."""
        chat_data = {'user_id': '12345', 'message': 'Hello, World!', 'timestamp': '2024-11-14T12:34:56'}

        mock_save_to_db.return_value = None 

        self.chat_model.save_chat(chat_data)

        self.mock_mongo_db['chats'].insert_one.assert_called_once_with(chat_data)

    @patch.object(ChatModel, 'find_one')
    def test_get_chat_success(self, mock_find_one):
        """Test case for retrieving a chat session successfully by its ID."""

        chat_id = '507f1f77bcf86cd799439011'
        mock_chat_data = {'_id': ObjectId(chat_id), 'user_id': '12345', 'message': 'Hello, World!', 'timestamp': '2024-11-14T12:34:56'}

        mock_find_one.return_value = mock_chat_data

        result = self.chat_model.get_chat(chat_id)

        self.assertEqual(result, mock_chat_data)


    def tearDown(self):
        """Clean up any necessary resources after each test."""
        # Any necessary clean-up can be done here (e.g., resetting mock data)
        pass


if __name__ == '__main__':
    unittest.main()
