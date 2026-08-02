"""
app/marks/__init__.py
==============================================================================
Project: College Student Performance Analytics System
Description: Marks Blueprint package initialization. Declares marks_bp for
             managing academic scores, exams, and grade evaluation.
==============================================================================
"""

from flask import Blueprint

marks_bp = Blueprint('marks', __name__)

from app.marks import routes  # noqa: E402, F401
