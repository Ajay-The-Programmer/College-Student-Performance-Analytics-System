"""
app/__init__.py
==============================================================================
Project: College Student Performance Analytics System
Description: Core application package initializer featuring the Flask Application
             Factory pattern (`create_app`), extension bindings, and Blueprint registration.
==============================================================================
"""

import os
from flask import Flask, render_template
from flask_login import login_required
from config import config_by_name
from app.extensions import db, login_manager


def create_app(config_name=None):
    """
    Application Factory Function.
    
    Creates, configures, and returns a Flask application instance.
    
    :param config_name: Environment configuration key ('development', 'testing', 'production')
    :return: Configured Flask application instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    # Initialize Flask app instance
    flask_app = Flask(__name__, instance_relative_config=False)
    
    # Load configuration settings
    flask_app.config.from_object(config_by_name[config_name])

    # Initialize Flask Extensions with App Instance
    db.init_app(flask_app)
    login_manager.init_app(flask_app)

    # Register database models & login user loader
    from app import models  # noqa: F401

    # Register Blueprints
    register_blueprints(flask_app)

    # Core Main Home Route
    @flask_app.route('/')
    def index():
        """Main Home Page displaying project overview and navigation."""
        return render_template('index.html')

    # Common Dashboard Route
    @flask_app.route('/dashboard')
    @login_required
    def dashboard():
        """Main Dashboard route for logged-in users."""
        return render_template('dashboard.html')

    # Error Handlers
    @flask_app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_title="404 - Page Not Found", error_message="The requested resource could not be found."), 404

    @flask_app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', error_title="500 - Internal Server Error", error_message="An unexpected error occurred. Please try again later."), 500

    return flask_app


def register_blueprints(flask_app):
    """
    Helper function to register all module Blueprints with the Flask app.
    
    :param flask_app: Flask app instance
    """
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.students import students_bp
    from app.attendance import attendance_bp
    from app.marks import marks_bp
    from app.analytics import analytics_bp
    from app.reports import reports_bp

    flask_app.register_blueprint(auth_bp, url_prefix='/auth')
    flask_app.register_blueprint(admin_bp, url_prefix='/admin')
    flask_app.register_blueprint(students_bp, url_prefix='/students')
    flask_app.register_blueprint(attendance_bp, url_prefix='/attendance')
    flask_app.register_blueprint(marks_bp, url_prefix='/marks')
    flask_app.register_blueprint(analytics_bp, url_prefix='/analytics')
    flask_app.register_blueprint(reports_bp, url_prefix='/reports')
