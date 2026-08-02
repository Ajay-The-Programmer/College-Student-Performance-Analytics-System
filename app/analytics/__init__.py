"""
app/analytics/__init__.py
==============================================================================
Project: College Student Performance Analytics System
Description: Analytics Blueprint package initialization. Declares analytics_bp
             for machine learning predictions and Plotly visualizations.
==============================================================================
"""

from flask import Blueprint

analytics_bp = Blueprint('analytics', __name__)

from app.analytics import routes  # noqa: E402, F401
