import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

from config import Config
from db.mongo_db import MongoDB
from db.redis import Redis
from error_handlers import ErrorHandler
from loggers.base_logger import BaseLogger
from routes.chat_blueprint import chat_blueprint
from routes.render_blueprint import render_blueprint
from routes.user_blueprint import user_blueprint
from services.socket_service import SocketService

BASEDIR = os.path.dirname(os.path.abspath(__file__))
app_logger = BaseLogger('app_logger')

def create_app(config_class=Config):
    """ Create and configure the Flask application. """
    app = Flask(__name__, template_folder=os.path.join(BASEDIR, 'templates'))
    app.config.from_object(config_class)

    @app.errorhandler(400)
    def handle_400_error(error):
        app_logger.error(f"400 Error: {error}")
        return ErrorHandler.handle_invalid_input(error)

    @app.errorhandler(404)
    def handle_404_error(error):
        app_logger.error(f"404 Error: {error}") 
        return ErrorHandler.handle_not_found(error)

    @app.errorhandler(500)
    def handle_500_error(error):
        app_logger.error(f"500 Error: {error}") 
        return ErrorHandler.handle_generic_error(error)

    # Initialize MongoDB and Redis connections
    mongo_db_connection  = MongoDB(app)
    redis_connenction = Redis(app)  

    # Initialize JWT Manager
    jwt = JWTManager(app)

    # Initialize SocketIO
    socketio = SocketIO(app,cors_allowed_origins="*")  # Attach SocketIO to the app  

    # Initialize the socket service and register socket event handlers
    socket_service = SocketService(socketio)
    socket_service.init_socket_handlers()

    # Register Blueprints
    app.register_blueprint(chat_blueprint)
    app.register_blueprint(render_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/auth')

    # Attach the MongoDB connection to the app context if needed
    with app.app_context():
        app.mongo_db = mongo_db_connection.get_db()  # Optional: Attach to app context for easy access
        app.redis = redis_connenction.get_redis()

    return app, socketio

if __name__ == "__main__":
    app, socketio = create_app()
    app_logger.info("Application started")
    socketio.run(app, debug=True)  # Use socketio to run the app




