import os
import unittest
from unittest.mock import MagicMock, patch
from models.user_model import UserModel, BaseModel
from exceptions import UserNotFoundException

class TestUserModel(unittest.TestCase):
    """Test case class for the UserModel class."""

    def setUp(self):
        """Set up the test environment by mocking the MongoDB connection."""
        self.mock_mongo_db = MagicMock()
        self.user_model = UserModel(username='testuser', password='password123', email='testuser@example.com', mongo_db=self.mock_mongo_db)

    def test_generate_random_avatar(self):
        """Test case for generating a random avatar."""
        avatar_path = self.user_model.generate_random_avatar()
        self.assertTrue(avatar_path.endswith('.png'))
        self.assertTrue(os.path.exists(avatar_path))
    
    @patch.object(BaseModel, 'save_to_db')
    def test_save_to_db(self,mock_save_to_db):
        """Test case for saving user to the database."""
        user_data = {
            'username': 'testuser',
            'password_hash': self.user_model.password_hash,
            'email': 'testuser@example.com',
            'avatar': self.user_model.avatar,
            'created_at': self.user_model.created_at,
            'last_active_at': self.user_model.last_active_at
        }
        
        mock_save_to_db.return_value = None

        self.user_model.save_to_db()

        mock_save_to_db.assert_called_once_with('users', user_data)

    @patch.object(BaseModel, 'find_one')
    def test_find_user(self, mock_find_one):
        """Test case for successfully finding a user."""
        user_data = {'username': 'testuser', 'email': 'testuser@example.com'}
        mock_find_one.return_value = user_data

        user = UserModel.find_user('testuser', self.mock_mongo_db)

        self.assertEqual(user['username'], 'testuser')

    @patch.object(BaseModel, 'find_one')
    def test_find_user_not_found(self, mock_find_one):
        """Test case for handling user not found."""
        mock_find_one.return_value = None

        with self.assertRaises(UserNotFoundException):
            UserModel.find_user('nonexistentuser', self.mock_mongo_db)

    def test_verify_password(self):
        """Test case for verifying the correct password."""
        password_check = self.user_model.verify_password('password123')
        self.assertTrue(password_check)


    def test_update_last_active(self):
        """Test case for updating the last active timestamp."""
        self.user_model.update_in_db = MagicMock(return_value=None)

        self.user_model.update_last_active()

        self.mock_mongo_db['users'].update_one.assert_called_once_with(
            {'username': 'testuser'},
            {'$set': {'last_active_at': self.user_model.last_active_at}}
        )

    def test_update_user(self):
        """Test case for updating user information."""
        update_data = {'email': 'newemail@example.com'}

        self.user_model.update_in_db = MagicMock(return_value=None)

        self.user_model.update_user(update_data)

        self.mock_mongo_db['users'].update_one.assert_called_once_with(
            {'username': 'testuser'},
            {'$set': update_data}
        )

    def tearDown(self):
        """Clean up any necessary resources after each test."""
        # Any necessary clean-up can be done here (e.g., resetting mock data)
        pass


if __name__ == '__main__':
    unittest.main()
