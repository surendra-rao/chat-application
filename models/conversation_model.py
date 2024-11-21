from bson.objectid import ObjectId
from models.base_model import BaseModel

class ConversationModel(BaseModel):
    """Model for managing conversations."""

    def __init__(self, mongo_db):
        super().__init__(mongo_db)

    def save_conversation(self, data):
        """Save a conversation to the database."""
        super().save_to_db('conversations', data)

    def get_conversation(self, conversation_id):
        """Retrieve a specific conversation by ID."""
        return self.find_one('conversations', {'_id': ObjectId(conversation_id)})