from flask_pymongo import PyMongo

class MongoDB:
    """ MongoDB Connection with Flask integration """
    def __init__(self, app=None):
        self.mongo = PyMongo()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """ Initialize the connection with a Flask app """
        self.mongo.init_app(app)

    def get_db(self):
        """ Get the MongoDB instance """
        return self.mongo.db