# error_handlers.py
from flask import jsonify,render_template

class ErrorHandler:
    @staticmethod
    def handle_invalid_input(error):
        """Handle invalid input errors (e.g., missing or invalid fields)."""
        return jsonify({"error": str(error)}), 400

    @staticmethod
    def handle_not_found(error):
        """Handle resource not found errors."""
        return jsonify({"error": "Resource not found: " + str(error)}), 404

    @staticmethod
    def handle_database_error(error):
        """Handle database-related errors."""
        return jsonify({"error": "Database error: " + str(error)}), 500

    @staticmethod
    def handle_generic_error(error):
        """Handle any other exceptions."""
        return jsonify({"error": "An error occurred: " + str(error)}), 500
    
    @staticmethod
    def handle_render_error(error):
        """Handle exceptions for routes that render HTML templates."""
        return render_template("error.html", error=str(error)), 500
