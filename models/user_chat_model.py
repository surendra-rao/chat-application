

from models.base_model import BaseModel 


class UserChatModel(BaseModel):
    """Model for managing user chat lists."""

    def __init__(self, mongo_db):
        """Initialize the UserChatListModel with a MongoDB connection."""
        super().__init__(mongo_db)  

    def save_user_chat(self, data):
        """Save a chat list to the database."""
        super().save_to_db('user_chat', data)

    def get_user_chat(self):
        """Retrieve the chat list, sorted by the most recent timestamp."""
        chat_list = self.mongo_db.user_chats.find().sort('timestamp', -1)
        return chat_list
