"""
app/models/__init__.py
==============================================================================
Project: College Student Performance Analytics System
Description: Package initializer for SQLAlchemy database models.
             Exports models for database migration detection.
==============================================================================
"""

from app.models.user import User

__all__ = ['User']
