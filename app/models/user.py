"""
app/models/user.py
==============================================================================
Project: College Student Performance Analytics System
Description: Database model definition for User accounts supporting Flask-Login
             UserMixin integration and role management (Admin, Student, Faculty).
==============================================================================
"""

from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    """
    User database model representing system users (Students, Admins, Faculty).
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student') # admin, student, faculty
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User username='{self.username}' role='{self.role}'>"


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader callback function.
    
    :param user_id: User database identifier
    :return: User object or None if not found
    """
    return User.query.get(int(user_id))
