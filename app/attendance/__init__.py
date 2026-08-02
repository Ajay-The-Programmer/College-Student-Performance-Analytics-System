"""
app/attendance/__init__.py
==============================================================================
Project: College Student Performance Analytics System
Description: Attendance Blueprint package initialization. Declares attendance_bp
             for tracking class attendance metrics.
==============================================================================
"""

from flask import Blueprint

attendance_bp = Blueprint('attendance', __name__)

from app.attendance import routes  # noqa: E402, F401
