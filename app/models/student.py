"""
app/models/student.py
==============================================================================
Project: College Student Performance Analytics System
Description: Database model for Student records and relationships.
==============================================================================
"""

from datetime import datetime
from app.extensions import db


class Student(db.Model):
    """
    Student model for storing student personal and academic profile details.
    Has one-to-many relationships with Attendance and Marks.
    """
    __tablename__ = 'students'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Student identification
    roll_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    # Academic details
    course = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    # Record timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships: One Student has many Attendance records and Marks records
    attendances = db.relationship('Attendance', backref='student', lazy=True, cascade='all, delete-orphan')
    marks = db.relationship('Marks', backref='student', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Student roll_number='{self.roll_number}' name='{self.first_name} {self.last_name}'>"
