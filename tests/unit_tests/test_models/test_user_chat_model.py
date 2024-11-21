import unittest
from unittest.mock import MagicMock
from models.user_chat_model import UserChatModel


class TestUserChatModel(unittest.TestCase):
    """Test case class for the UserChatModel class."""

    def setUp(self):
        """Set up the test environment by mocking the MongoDB connection."""
        self.mock_mongo_db = MagicMock()
        self.user_chat_model = UserChatModel(self.mock_mongo_db)
        setattr(self.user_chat_model, 'mongo_db', self.mock_mongo_db)

    def test_save_user_chat(self):
        """Test case for saving a user chat successfully."""
        user_chat_data = {
            'user_id': 'user1',
            'chat_id': '507f1f77bcf86cd799439011',
            'timestamp': '2024-11-14T12:34:56'
        }

        self.user_chat_model.save_to_db = MagicMock(return_value=None)  # Simulate success

        self.user_chat_model.save_user_chat(user_chat_data)

        self.mock_mongo_db['user_chat'].insert_one.assert_called_once_with(user_chat_data)


    def test_get_user_chat(self):
        """Test case for retrieving user chat list successfully."""
        mock_chat_list = [
            {'user_id': 'user1', 'chat_id': '507f1f77bcf86cd799439011', 'timestamp': '2024-11-14T12:34:56'},
            {'user_id': 'user1', 'chat_id': '507f1f77bcf86cd799439012', 'timestamp': '2024-11-14T12:35:56'}
        ]

        self.mock_mongo_db.user_chats.find.return_value.sort.return_value = mock_chat_list

        result = self.user_chat_model.get_user_chat()

        self.assertEqual(result, mock_chat_list)



    def tearDown(self):
        """Clean up any necessary resources after each test."""
        # Any necessary clean-up can be done here (e.g., resetting mock data)
        pass


if __name__ == '__main__':
    unittest.main()
