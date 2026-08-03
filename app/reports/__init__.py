"""
app/reports/__init__.py
==============================================================================
Project: College Student Performance Analytics System
Description: Reports Blueprint package initialization.
==============================================================================
"""

from flask import Blueprint

reports_bp = Blueprint('reports', __name__)

from app.reports import routes  # noqa: E402, F401
