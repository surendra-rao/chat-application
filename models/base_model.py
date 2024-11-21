# base_model.py

from exceptions import DatabaseConnectionException
from loggers.connection_logger import ConnectionLogger


class BaseModel:
    """
    Base model class to provide common functionality for all models.
    """
    def __init__(self, mongo_db):
        """Initialize with a MongoDB connection and set up a logger."""
        self.mongo_db = mongo_db
        self.logger = ConnectionLogger()  

    def save_to_db(self, collection_name, data):
        """Save data to a specified collection."""
        try:
            self.mongo_db[collection_name].insert_one(data)
        except Exception as e:
            self.logger.error(f"Failed to save data to {collection_name}: {e}")
            raise DatabaseConnectionException(f"Error saving to {collection_name}: {str(e)}")

    def find_one(self, collection_name, query):
        """Find a document in a specified collection."""
        try:
            document = self.mongo_db[collection_name].find_one(query)
            return document
        except Exception as e:
            self.logger.error(f"Failed to retrieve data from {collection_name}: {e}")
            raise DatabaseConnectionException(f"Error retrieving from {collection_name}: {str(e)}")
    
    def update_in_db(self, collection_name, query, update_data):
        """Update a document in a specified collection."""
        try:
            result = self.mongo_db[collection_name].update_one(query, {'$set': update_data})
            if not result.matched_count:
                self.logger.warning(f"No document matched for update in {collection_name} with query {query}")

        except Exception as e:
            self.logger.error(f"Failed to update data in {collection_name}: {e}")
            raise DatabaseConnectionException(f"Error updating in {collection_name}: {str(e)}")

    def delete_from_db(self, collection_name, query):
        """Delete a document from a specified collection."""
        try:
            result = self.mongo_db[collection_name].delete_one(query)
            if not result.deleted_count:
                self.logger.warning(f"No document matched for deletion in {collection_name} with query {query}")
        except Exception as e:
            self.logger.error(f"Failed to delete document from {collection_name}: {e}")
            raise DatabaseConnectionException(f"Error deleting from {collection_name}: {str(e)}")
