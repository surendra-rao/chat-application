import unittest
from unittest.mock import MagicMock, patch
from models.conversation_model import ConversationModel
from bson.objectid import ObjectId


class TestConversationModel(unittest.TestCase):
    """Test case class for the ConversationModel class."""

    def setUp(self):
        """Set up the test environment by mocking the MongoDB connection."""
        self.mock_mongo_db = MagicMock()
        self.conversation_model = ConversationModel(self.mock_mongo_db)

    @patch.object(ConversationModel, 'save_to_db')
    def test_save_conversation(self, mock_save_to_db):
        """Test case for saving a conversation successfully."""

        conversation_data = {'user_ids': ['12345', '67890'], 'messages': ['Hello', 'How are you?'], 'timestamp': '2024-11-14T12:34:56'}

        mock_save_to_db.return_value = None 

        self.conversation_model.save_conversation(conversation_data)

        self.mock_mongo_db['conversations'].insert_one.assert_called_once_with(conversation_data)


    @patch.object(ConversationModel, 'find_one')
    def test_get_conversation(self, mock_find_one):
        """Test case for retrieving a conversation successfully by its ID."""

        conversation_id = '507f1f77bcf86cd799439011'
        mock_conversation_data = {'_id': ObjectId(conversation_id), 'user_ids': ['12345', '67890'], 'messages': ['Hello', 'How are you?'], 'timestamp': '2024-11-14T12:34:56'}

        mock_find_one.return_value = mock_conversation_data

        result = self.conversation_model.get_conversation(conversation_id)

        self.assertEqual(result, mock_conversation_data)


    def tearDown(self):
        """Clean up any necessary resources after each test."""
        # Any necessary clean-up can be done here (e.g., resetting mock data)
        pass


if __name__ == '__main__':
    unittest.main()
