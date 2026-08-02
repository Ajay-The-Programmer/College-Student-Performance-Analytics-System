"""
app/models/attendance.py
==============================================================================
Project: College Student Performance Analytics System
Description: Database model for Student Attendance records.
==============================================================================
"""

from datetime import date, datetime
from app.extensions import db


class Attendance(db.Model):
    """
    Attendance model representing student daily class presence or absence.
    Belongs to a Student and a Subject via foreign keys.
    """
    __tablename__ = 'attendance'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)

    # Attendance details
    attendance_date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(10), nullable=False)  # 'Present' or 'Absent'

    # Record timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Attendance student_id={self.student_id} subject_id={self.subject_id} status='{self.status}'>"
