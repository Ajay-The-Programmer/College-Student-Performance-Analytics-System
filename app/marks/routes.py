"""
app/marks/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Marks Blueprint route handlers (Academic Scores, Exam Entry, Grade Sheet).
==============================================================================
"""

from flask import render_template
from app.marks import marks_bp


@marks_bp.route('/')
def overview():
    """Render Academic Marks Overview."""
    return render_template('marks/overview.html')


@marks_bp.route('/enter', methods=['GET', 'POST'])
def enter_marks():
    """Render Enter Marks Form."""
    return render_template('marks/enter.html')


@marks_bp.route('/report-card/<int:student_id>')
def report_card(student_id):
    """Render Student Report Card / Transcript."""
    return render_template('marks/report_card.html', student_id=student_id)
