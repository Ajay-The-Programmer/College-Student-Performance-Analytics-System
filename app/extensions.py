"""
app/extensions.py
==============================================================================
Project: College Student Performance Analytics System
Description: Instantiates Flask extensions (SQLAlchemy, Flask-Migrate, Flask-Login)
             outside of the application factory to avoid circular imports.
==============================================================================
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize extension instances without binding to an app yet
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Configure Flask-Login defaults (login view endpoint name)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
