import os
from flask import Blueprint, render_template

from loggers.message_logger import MessageLogger
from error_handlers import ErrorHandler

BASEDIR = os.path.dirname(os.path.abspath(__file__))

# Create a Blueprint for rendering routes
render_blueprint = Blueprint('render', __name__, template_folder=os.path.join(BASEDIR, 'templates'))

# Initialize message logger
message_logger = MessageLogger()

# Error handler for rendering exceptions
@render_blueprint.errorhandler(Exception)
def handle_render_exception(error):
    """Handle exceptions in render routes."""
    message_logger.error(f"Rendering error: {error}") 
    return ErrorHandler.handle_render_error(error)

@render_blueprint.route('/chat')
def chat_view():
    """Render chat page."""
    try:
        return render_template("chat.html")
    except Exception as e:
        message_logger.error(f"Error rendering chat page: {e}") 
        return handle_render_exception(e)

@render_blueprint.route('/')
def index():
    """Render login page."""
    try:
        return render_template("login.html")
    except Exception as e:
        message_logger.error(f"Error rendering login page: {e}") 
        return handle_render_exception(e)

@render_blueprint.route('/home')
def home():
    """Render home page."""
    try:
        return render_template("home.html")
    except Exception as e:
        message_logger.error(f"Error rendering home page: {e}")
        return handle_render_exception(e)
