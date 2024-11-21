import unittest
from unittest.mock import MagicMock, patch
from models.base_model import BaseModel
from exceptions import DatabaseConnectionException
from loggers.connection_logger import ConnectionLogger


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        # Mock MongoDB connection
        self.mock_mongo_db = MagicMock()
        self.model = BaseModel(self.mock_mongo_db)

    @patch.object(ConnectionLogger, 'error')
    def test_save_to_db_success(self, mock_error):
        collection_name = 'users'
        data = {'name': 'test user', 'email': 'test@example.com'}

        self.mock_mongo_db[collection_name].insert_one = MagicMock()
        self.model.save_to_db(collection_name, data)

        self.mock_mongo_db[collection_name].insert_one.assert_called_once_with(data)
        mock_error.assert_not_called()

    @patch.object(ConnectionLogger, 'error')
    def test_save_to_db_failure(self, mock_error):
        collection_name = 'users'
        data = {'name': 'test user', 'email': 'test@example.com'}

        self.mock_mongo_db[collection_name].insert_one = MagicMock(side_effect=Exception('DB error'))

        with self.assertRaises(DatabaseConnectionException):
            self.model.save_to_db(collection_name, data)

        mock_error.assert_called_once_with(f"Failed to save data to {collection_name}: DB error")

    @patch.object(ConnectionLogger, 'error')
    def test_find_one_success(self, mock_error):
        collection_name = 'users'
        query = {'email': 'test@example.com'}
        mock_document = {'name': 'test user', 'email': 'test@example.com'}

        self.mock_mongo_db[collection_name].find_one = MagicMock(return_value=mock_document)

        result = self.model.find_one(collection_name, query)

        self.assertEqual(result, mock_document)
        mock_error.assert_not_called()

    @patch.object(ConnectionLogger, 'error')
    def test_find_one_failure(self, mock_error):
        collection_name = 'users'
        query = {'email': 'test@example.com'}

        self.mock_mongo_db[collection_name].find_one = MagicMock(side_effect=Exception('DB error'))

        with self.assertRaises(DatabaseConnectionException):
            self.model.find_one(collection_name, query)

        mock_error.assert_called_once_with(f"Failed to retrieve data from {collection_name}: DB error")

    @patch.object(ConnectionLogger, 'warning')
    @patch.object(ConnectionLogger, 'error')
    def test_update_in_db_success(self, mock_error, mock_warning):
        collection_name = 'users'
        query = {'email': 'test@example.com'}
        update_data = {'name': 'updated user'}

        result_mock = MagicMock()
        result_mock.matched_count = 1  
        self.mock_mongo_db[collection_name].update_one = MagicMock(return_value=result_mock)

        self.model.update_in_db(collection_name, query, update_data)

        self.mock_mongo_db[collection_name].update_one.assert_called_once_with(query, {'$set': update_data})

        mock_warning.assert_not_called()
        mock_error.assert_not_called()

    @patch.object(ConnectionLogger, 'warning')
    @patch.object(ConnectionLogger, 'error')
    def test_update_in_db_failure(self, mock_error, mock_warning):
        collection_name = 'users'
        query = {'email': 'test@example.com'}
        update_data = {'name': 'updated user'}

        self.mock_mongo_db[collection_name].update_one = MagicMock(side_effect=Exception('DB error'))

        with self.assertRaises(DatabaseConnectionException):
            self.model.update_in_db(collection_name, query, update_data)

        mock_error.assert_called_once_with(f"Failed to update data in {collection_name}: DB error")

    @patch.object(ConnectionLogger, 'warning')
    @patch.object(ConnectionLogger, 'error')
    def test_delete_from_db_success(self, mock_error, mock_warning):
        collection_name = 'users'
        query = {'email': 'test@example.com'}

        result_mock = MagicMock()
        result_mock.deleted_count = 1 
        self.mock_mongo_db[collection_name].delete_one = MagicMock(return_value=result_mock)

        self.model.delete_from_db(collection_name, query)

        self.mock_mongo_db[collection_name].delete_one.assert_called_once_with(query)

        mock_warning.assert_not_called()
        mock_error.assert_not_called()

    @patch.object(ConnectionLogger, 'warning')
    @patch.object(ConnectionLogger, 'error')
    def test_delete_from_db_failure(self, mock_error, mock_warning):
        collection_name = 'users'
        query = {'email': 'test@example.com'}

        self.mock_mongo_db[collection_name].delete_one = MagicMock(side_effect=Exception('DB error'))

        with self.assertRaises(DatabaseConnectionException):
            self.model.delete_from_db(collection_name, query)

        mock_error.assert_called_once_with(f"Failed to delete document from {collection_name}: DB error")

    @patch.object(ConnectionLogger, 'warning')
    def test_update_in_db_no_match(self, mock_warning):
        collection_name = 'users'
        query = {'email': 'test@example.com'}
        update_data = {'name': 'updated user'}

        result_mock = MagicMock()
        result_mock.matched_count = 0  
        self.mock_mongo_db[collection_name].update_one = MagicMock(return_value=result_mock)

        self.model.update_in_db(collection_name, query, update_data)

        mock_warning.assert_called_once_with(f"No document matched for update in {collection_name} with query {query}")


if __name__ == '__main__':
    unittest.main()
