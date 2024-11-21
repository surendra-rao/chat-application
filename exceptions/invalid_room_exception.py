

class InvalidRoomException(Exception):
    """Exception raised when attempting to access or send a message to an invalid room."""
    def __init__(self, room_id, message="Invalid room"):
        self.room_id = room_id
        super().__init__(f"{message}: {room_id}")