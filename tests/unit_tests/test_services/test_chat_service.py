import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from services.chat_service import ChatService

class TestChatService(unittest.TestCase):

    @patch('services.chat_service.MessageModel')
    def test_send_message(self, MockMessageModel):
        # Setup mock MongoDB and MessageModel
        mongo_db = MagicMock()
        mock_message_model_instance = MockMessageModel.return_value
        mock_message_model_instance.save_message.return_value = None

        # Call send_message
        response = ChatService.send_message(
            username="test_user",
            room_id="room_1",
            message_text="Hello, world!",
            mongo_db=mongo_db
        )

        # Assertions
        self.assertEqual(response["msg"], "Message sent successfully")
        self.assertEqual(response["status"], 200)
        mock_message_model_instance.save_message.assert_called_once()
        

    @patch('services.chat_service.MessageModel')
    def test_get_chat_history(self, MockMessageModel):
        # Setup mock MongoDB
        mongo_db = MagicMock()

        # Define sample messages returned by the mock
        sample_messages = [
            {
                '_id': '1',
                'username': 'user1',
                'room_id': 'room_1',
                'message': 'Test message 1',
                'timestamp': datetime(2024, 11, 13, 15, 30, tzinfo=timezone.utc)
            },
            {
                '_id': '2',
                'username': 'user2',
                'room_id': 'room_1',
                'message': 'Test message 2',
                'timestamp': datetime(2024, 11, 13, 15, 31, tzinfo=timezone.utc)
            },
        ]

        mock_find = MagicMock()
        mock_sort = MagicMock()
        mock_skip = MagicMock()
        mock_limit = MagicMock()

        # Setting the chained methods to return the sample messages
        mock_find.sort.return_value = mock_sort
        mock_sort.skip.return_value = mock_skip
        mock_skip.limit.return_value = sample_messages

        # Configure the mock to return the find method
        mongo_db.messages.find.return_value = mock_find

        # Call get_chat_history and convert generator to list
        chat_history = list(ChatService.get_chat_history(
            room_id="room_1",
            current_user="user1",
            mongo_db=mongo_db,
            page_size=50,
            page_num=1
        ))

        # Assertions
        self.assertEqual(len(chat_history), 2)
        self.assertEqual(chat_history[0]["username"], "user1")
        self.assertEqual(chat_history[0]["isSent"], True)
        self.assertEqual(chat_history[1]["username"], "user2")
        self.assertEqual(chat_history[1]["text"], "Test message 2")
        self.assertEqual(chat_history[1]["isSent"], False)

if __name__ == '__main__':
    unittest.main()
