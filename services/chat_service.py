from datetime import datetime,timezone

from models.message_model import MessageModel

class ChatService:
    """
    Service layer responsible for chat-related business logic.
    """

    @staticmethod
    def send_message( username, room_id, message_text,mongo_db):
        message_data = {
            'username': username,
            'room_id': room_id,
            'message': message_text,
            'timestamp': datetime.now(timezone.utc)
        }
        message = MessageModel(mongo_db)
        message.save_message(message_data)
        return {"msg": "Message sent successfully", "status": 200}
    
    @staticmethod
    def get_chat_history(room_id, current_user,  mongo_db, page_size=50, page_num=1):
        messages = MessageModel(mongo_db)
        skip = (page_num - 1) * page_size
        # messages = messages.get_messages(room_id)
        messages = mongo_db.messages.find({"room_id": room_id}).sort('timestamp', -1).skip(skip).limit(page_size)
        
        for message in messages:
            transformed_message = {
                "id": str(message['_id']),
                "username": message['username'],
                "room_id": message['room_id'],
                "text": message['message'],
                "time": message['timestamp'].strftime("%H:%M"),  # Format timestamp to "HH:MM"
                "isSent": message['username'] == current_user  # True if the message is from the current user
            }
            yield transformed_message