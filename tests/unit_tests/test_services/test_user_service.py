import unittest
from unittest.mock import MagicMock, patch
from services.user_service import UserService
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

class TestUserService(unittest.TestCase):

    @patch('services.user_service.UserModel')
    def test_register_user_user_exists(self, MockUserModel):
        # Mock the find_user method to return a user, simulating "User already exists"
        MockUserModel.find_user.return_value = {"username": "existing_user"}

        # Call register_user
        response = UserService.register_user(
            username="existing_user",
            password="password123",
            email="test@example.com",
            mongo_db=MagicMock()
        )

        # Assertions
        self.assertEqual(response["msg"], "User already exists")
        self.assertEqual(response["status"], 404)

    @patch('services.user_service.UserModel')
    def test_register_user_successful(self, MockUserModel):
        # Mock find_user to return None, simulating no user found
        MockUserModel.find_user.return_value = None
        mock_user_instance = MockUserModel.return_value
        mock_user_instance.save_to_db.return_value = None

        # Call register_user
        response = UserService.register_user(
            username="new_user",
            password="password123",
            email="test@example.com",
            mongo_db=MagicMock()
        )

        # Assertions
        self.assertEqual(response["msg"], "User registered successfully")
        self.assertEqual(response["status"], 201)
        mock_user_instance.save_to_db.assert_called_once()

    @patch('services.user_service.UserModel')
    @patch('services.user_service.check_password_hash')
    def test_authenticate_user_invalid_credentials(self, mock_check_password_hash, MockUserModel):
        # Mock find_user to return a user
        MockUserModel.find_user.return_value = {
            "username": "test_user",
            "password_hash": generate_password_hash("wrong_password"),
            "password" : "wrong_password"
        }

        # Mock check_password_hash to return False
        mock_check_password_hash.return_value = False

        # Call authenticate_user
        response = UserService.authenticate_user(
            username="test_user",
            password="password123",
            mongo_db=MagicMock()
        )

        # Assertions
        self.assertEqual(response["msg"], "Invalid credentials")
        self.assertEqual(response["status"], 401)

    @patch('services.user_service.UserModel')
    @patch('services.user_service.check_password_hash')
    @patch('services.user_service.create_access_token')
    def test_authenticate_user_successful(self, mock_create_access_token, mock_check_password_hash, MockUserModel):
        # Mock find_user to return a user with a hashed password
        MockUserModel.find_user.return_value = {
            "username": "test_user",
            "password_hash": generate_password_hash("password123")
        }

        # Mock check_password_hash to return True
        mock_check_password_hash.return_value = True

        # Mock create_access_token to return a fake token
        mock_create_access_token.return_value = "fake_token"

        # Call authenticate_user
        response = UserService.authenticate_user(
            username="test_user",
            password="password123",
            mongo_db=MagicMock()
        )

        # Assertions
        self.assertEqual(response["access_token"], "fake_token")
        self.assertEqual(response["status"], 200)
        mock_create_access_token.assert_called_once_with(identity="test_user")

    @patch('services.user_service.UserModel')
    def test_update_last_active_user_not_found(self, MockUserModel):
        # Mock find_user to return None, simulating "User not found"
        MockUserModel.find_user.return_value = None

        # Call update_last_active
        response = UserService.update_last_active(
            username="nonexistent_user",
            mongo_db=MagicMock()
        )

        # Assertions
        self.assertEqual(response["msg"], "User not found")
        self.assertEqual(response["status"], 404)

    @patch('services.user_service.UserModel')
    def test_update_last_active_successful(self, MockUserModel):
        # Mock find_user to return a user
        MockUserModel.find_user.return_value = {
            "username": "test_user",
            "password_hash": "hashed_password",
            "email": "test@example.com"
        }
        mock_user_instance = MockUserModel.return_value
        mock_user_instance.update_last_active.return_value = None

        # Call update_last_active
        response = UserService.update_last_active(
            username="test_user",
            mongo_db=MagicMock()
        )

        # Assertions
        self.assertEqual(response["msg"], "User's last active timestamp updated")
        self.assertEqual(response["status"], 200)
        mock_user_instance.update_last_active.assert_called_once()

    @patch('services.user_service.UserModel')
    def test_user_home_page_details_user_not_found(self, MockUserModel):
        # Mock find_user to return None, simulating "User not found"
        MockUserModel.find_user.return_value = None

        # Call user_home_page_details
        response = UserService.user_home_page_details(
            username="nonexistent_user",
            mongo_db=MagicMock()
        )

        # Assertions
        self.assertEqual(response["msg"], "User not found")
        self.assertEqual(response["status"], 404)

    @patch('services.user_service.UserModel')
    def test_user_home_page_details_successful(self, MockUserModel):
        # Mock find_user to return a user with sample data
        MockUserModel.find_user.return_value = {
            "_id": "12345",
            "username": "test_user",
            "avatar": "avatar.png"
        }

        # Call user_home_page_details
        response = UserService.user_home_page_details(
            username="test_user",
            mongo_db=MagicMock()
        )

        # Assertions
        self.assertEqual(response["msg"], "Token is valid")
        self.assertEqual(response["id"], "12345")
        self.assertEqual(response["avatar"], "avatar.png")
        self.assertEqual(response["name"], "test_user")
        self.assertEqual(response["status"], 200)

if __name__ == '__main__':
    unittest.main()
