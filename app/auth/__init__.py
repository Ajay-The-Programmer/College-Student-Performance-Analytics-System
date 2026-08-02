"""
app/auth/__init__.py
==============================================================================
Project: College Student Performance Analytics System
Description: Authentication Blueprint package initialization. Declares the auth_bp
             Blueprint instance for authentication routes.
==============================================================================
"""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from app.auth import routes  # noqa: E402, F401
