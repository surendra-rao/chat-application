
from models.base_model import BaseModel
from bson.objectid import ObjectId


class ChatModel(BaseModel):
    """Model for managing chat sessions."""

    def save_chat(self, data):
        """Save a chat session to the database."""
        super().save_to_db('chats', data)

    def get_chat(self, chat_id):
        """Retrieve a specific chat session by ID."""
        return self.find_one('chats', {'_id': ObjectId(chat_id)})