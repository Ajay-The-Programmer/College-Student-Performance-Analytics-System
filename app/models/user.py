"""
app/models/user.py
==============================================================================
Project: College Student Performance Analytics System
Description: Database model for User accounts (Admin and Faculty login).
==============================================================================
"""

from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    """
    User model representing system users (Admin and Faculty).
    """
    __tablename__ = 'users'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # User credentials
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    # User role: 'admin' or 'faculty'
    role = db.Column(db.String(20), nullable=False, default='faculty')

    # Account creation timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User username='{self.username}' role='{self.role}'>"


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader callback function.
    """
    return User.query.get(int(user_id))
