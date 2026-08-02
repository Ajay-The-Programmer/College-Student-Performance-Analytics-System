"""
app/models/__init__.py
==============================================================================
Project: College Student Performance Analytics System
Description: Package initializer importing all SQLAlchemy database models.
==============================================================================
"""

from app.models.user import User
from app.models.student import Student
from app.models.subject import Subject
from app.models.attendance import Attendance
from app.models.marks import Marks

__all__ = ['User', 'Student', 'Subject', 'Attendance', 'Marks']
