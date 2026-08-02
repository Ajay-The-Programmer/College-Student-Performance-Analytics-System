"""
app/models/subject.py
==============================================================================
Project: College Student Performance Analytics System
Description: Database model for Subject / Course details.
==============================================================================
"""

from app.extensions import db


class Subject(db.Model):
    """
    Subject model representing college subjects taught in semesters.
    Has one-to-many relationships with Attendance and Marks.
    """
    __tablename__ = 'subjects'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Subject details
    subject_code = db.Column(db.String(20), unique=True, nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    # Relationships: One Subject has many Attendance records and Marks records
    attendances = db.relationship('Attendance', backref='subject', lazy=True, cascade='all, delete-orphan')
    marks = db.relationship('Marks', backref='subject', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Subject code='{self.subject_code}' name='{self.subject_name}'>"
