"""
app/students/__init__.py
==============================================================================
Project: College Student Performance Analytics System
Description: Students Blueprint package initialization. Declares students_bp
             for student directory and profile management.
==============================================================================
"""

from flask import Blueprint

students_bp = Blueprint('students', __name__)

from app.students import routes  # noqa: E402, F401
