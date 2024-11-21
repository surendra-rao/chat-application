
from bson.objectid import ObjectId
from models.base_model import BaseModel


class GroupModel(BaseModel):
    """Model for managing groups."""

    def __init__(self, mongo_db):
        super().__init__(mongo_db)

    def save_group(self, data):
        """Save a group to the database."""
        super().save_to_db('groups', data)

    def get_group(self, group_id):
        """Retrieve a specific group by ID."""
        return self.find_one('groups', {'_id': ObjectId(group_id)})