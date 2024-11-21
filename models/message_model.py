from exceptions import DatabaseConnectionException
from exceptions import InvalidRoomException
from models.base_model import BaseModel

class MessageModel(BaseModel):
    """Model for managing individual messages in chats."""

    def __init__(self, mongo_db):
        super().__init__(mongo_db)

    def save_message(self, data):
        """Save a message to the database."""
        super().save_to_db('messages', data)

    def get_messages(self, room_id):
        """Retrieve messages, sorted by the most recent timestamp."""
        messages = list(self.mongo_db.messages.find({"room_id": room_id}).sort('timestamp', -1))
        if not messages:
            raise InvalidRoomException(f"No messages found for room ID {room_id}")
        return messages