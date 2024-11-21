import unittest
from unittest.mock import MagicMock, patch
from models.group_model import GroupModel
from bson.objectid import ObjectId


class TestGroupModel(unittest.TestCase):
    """Test case class for the GroupModel class."""

    def setUp(self):
        """Set up the test environment by mocking the MongoDB connection."""
        self.mock_mongo_db = MagicMock()
        self.group_model = GroupModel(self.mock_mongo_db)

    @patch.object(GroupModel, 'save_to_db')
    def test_save_group(self, mock_save_to_db):
        """Test case for saving a group successfully."""
        group_data = {
            'group_name': 'Chat Group 1',
            'members': ['user1', 'user2', 'user3'],
            'created_at': '2024-11-14T12:34:56'
        }

        mock_save_to_db.return_value = None

        self.group_model.save_group(group_data)

        self.mock_mongo_db['groups'].insert_one.assert_called_once_with(group_data)

    @patch.object(GroupModel, 'find_one')
    def test_get_group(self, mock_find_one):
        """Test case for retrieving a group successfully by its ID."""

        group_id = '507f1f77bcf86cd799439011'
        mock_group_data = {
            '_id': ObjectId(group_id),
            'group_name': 'Chat Group 1',
            'members': ['user1', 'user2', 'user3'],
            'created_at': '2024-11-14T12:34:56'
        }

        mock_find_one.return_value = mock_group_data

        result = self.group_model.get_group(group_id)
        self.assertEqual(result, mock_group_data)

    def tearDown(self):
        """Clean up any necessary resources after each test."""
        # Any necessary clean-up can be done here (e.g., resetting mock data)
        pass


if __name__ == '__main__':
    unittest.main()
