"""
Main Flask Application for AIPS Backend
---------------------------------------

Registers:
 - Domain Routes
 - Company Routes
 - Test Routes
 - Attempt Routes
 - Auth Routes

Loads Firebase, config, CORS, and logging.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import logging

# Import settings
from backend.config.settings import settings

# Import blueprints
from backend.routes.domain_routes import bp as domain_bp
from backend.routes.company_routes import bp as company_bp
from backend.routes.test_routes import bp as test_bp
from backend.routes.attempt_routes import bp as attempt_bp
from backend.routes.auth_routes import bp as auth_bp


def create_app():
    app = Flask(__name__)

    # Enable CORS for frontends (like Streamlit)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Logging setup
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Register all blueprints
    app.register_blueprint(domain_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(attempt_bp)
    app.register_blueprint(auth_bp)

    # Root route
    @app.route("/")
    def home():
        return jsonify({
            "message": "AIPS Backend Running",
            "status": "online"
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG
    )
