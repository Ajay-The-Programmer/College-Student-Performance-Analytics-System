"""
app/attendance/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Attendance Blueprint route handlers (Overview, Mark Attendance, Reports).
==============================================================================
"""

from flask import render_template
from app.attendance import attendance_bp


@attendance_bp.route('/')
def overview():
    """Render Attendance Overview & Metrics."""
    return render_template('attendance/overview.html')


@attendance_bp.route('/mark', methods=['GET', 'POST'])
def mark_attendance():
    """Render Mark Attendance Form."""
    return render_template('attendance/mark.html')


@attendance_bp.route('/report')
def report():
    """Render Attendance Reports & Analytics."""
    return render_template('attendance/report.html')
