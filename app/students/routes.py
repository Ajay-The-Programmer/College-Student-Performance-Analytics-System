"""
app/students/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Students Blueprint route handlers (Student Directory, Profile, Add Student).
==============================================================================
"""

from flask import render_template
from app.students import students_bp


@students_bp.route('/')
@students_bp.route('/list')
def index():
    """Render Student Directory List."""
    return render_template('students/index.html')


@students_bp.route('/<int:student_id>')
def detail(student_id):
    """Render Student Profile Detail View."""
    return render_template('students/detail.html', student_id=student_id)


@students_bp.route('/add', methods=['GET', 'POST'])
def add_student():
    """Render Add Student Record Form."""
    return render_template('students/add.html')
