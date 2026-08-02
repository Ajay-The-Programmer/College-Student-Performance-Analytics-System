"""
app/admin/__init__.py
==============================================================================
Project: College Student Performance Analytics System
Description: Admin Blueprint package initialization. Declares the admin_bp
             Blueprint instance for administrative routes.
==============================================================================
"""

from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

from app.admin import routes  # noqa: E402, F401
