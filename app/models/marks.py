"""
app/models/marks.py
==============================================================================
Project: College Student Performance Analytics System
Description: Database model for Student Marks / Exam Scores.
==============================================================================
"""

from datetime import datetime
from app.extensions import db


class Marks(db.Model):
    """
    Marks model representing internal, external, and total exam scores.
    Belongs to a Student and a Subject via foreign keys.
    """
    __tablename__ = 'marks'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)

    # Marks details
    internal_marks = db.Column(db.Float, nullable=False, default=0.0)
    external_marks = db.Column(db.Float, nullable=False, default=0.0)

    # Record timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Marks student_id={self.student_id} subject_id={self.subject_id}>"
