"""
app/students/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Student Management Blueprint route handlers (CRUD operations,
             search filtering, SQLAlchemy pagination, and validation).
==============================================================================
"""

from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.students import students_bp
from app.extensions import db
from app.models.student import Student


@students_bp.route('/')
@students_bp.route('/list')
@login_required
def index():
    """
    Display paginated list of students with search filtering.
    """
    search_query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)

    query = Student.query
    total_students = Student.query.count()

    if search_query:
        query = query.filter(
            (Student.roll_number.ilike(f"%{search_query}%")) |
            (Student.first_name.ilike(f"%{search_query}%")) |
            (Student.last_name.ilike(f"%{search_query}%")) |
            (Student.department.ilike(f"%{search_query}%"))
        )

    pagination = query.order_by(Student.roll_number.asc()).paginate(
        page=page, per_page=10, error_out=False
    )
    students = pagination.items

    return render_template(
        'students/index.html',
        students=students,
        pagination=pagination,
        search_query=search_query,
        total_students=total_students
    )


@students_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """
    Add a new student record to the database.
    """
    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        gender = request.form.get('gender', '').strip()
        dob_str = request.form.get('date_of_birth', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        course = request.form.get('course', '').strip()
        department = request.form.get('department', '').strip()
        semester_str = request.form.get('semester', '').strip()

        # Validations
        errors = []

        if not roll_number:
            errors.append('Roll Number is required.')
        elif Student.query.filter_by(roll_number=roll_number).first():
            errors.append('Roll Number already exists.')

        if not first_name or not last_name:
            errors.append('First Name and Last Name are required.')

        if not department:
            errors.append('Department is required.')

        # Semester validation (1 - 8)
        try:
            semester = int(semester_str)
            if semester < 1 or semester > 8:
                errors.append('Semester must be an integer between 1 and 8.')
        except ValueError:
            errors.append('Semester must be a valid number between 1 and 8.')

        # Phone digits validation
        if phone and not phone.isdigit():
            errors.append('Phone number must contain digits only.')

        # Email format validation
        if email and '@' not in email:
            errors.append('Please provide a valid email address.')

        # Date of birth parsing
        date_of_birth = None
        if dob_str:
            try:
                date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Invalid date format for Date of Birth.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('students/form.html', student=request.form, action='Add')

        # Create and save new student instance
        new_student = Student(
            roll_number=roll_number,
            first_name=first_name,
            last_name=last_name,
            gender=gender if gender else None,
            date_of_birth=date_of_birth,
            email=email if email else None,
            phone=phone if phone else None,
            course=course if course else None,
            department=department,
            semester=semester
        )

        db.session.add(new_student)
        db.session.commit()

        flash('Student Added Successfully', 'success')
        return redirect(url_for('students.index'))

    return render_template('students/form.html', student=None, action='Add')


@students_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    """
    Edit existing student record.
    """
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        gender = request.form.get('gender', '').strip()
        dob_str = request.form.get('date_of_birth', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        course = request.form.get('course', '').strip()
        department = request.form.get('department', '').strip()
        semester_str = request.form.get('semester', '').strip()

        errors = []

        if not roll_number:
            errors.append('Roll Number is required.')
        else:
            existing = Student.query.filter(
                Student.roll_number == roll_number,
                Student.id != id
            ).first()
            if existing:
                errors.append('Roll Number already exists for another student.')

        if not first_name or not last_name:
            errors.append('First Name and Last Name are required.')

        if not department:
            errors.append('Department is required.')

        try:
            semester = int(semester_str)
            if semester < 1 or semester > 8:
                errors.append('Semester must be an integer between 1 and 8.')
        except ValueError:
            errors.append('Semester must be a valid number between 1 and 8.')

        if phone and not phone.isdigit():
            errors.append('Phone number must contain digits only.')

        if email and '@' not in email:
            errors.append('Please provide a valid email address.')

        date_of_birth = None
        if dob_str:
            try:
                date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Invalid date format for Date of Birth.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('students/form.html', student=student, action='Edit')

        # Update student attributes
        student.roll_number = roll_number
        student.first_name = first_name
        student.last_name = last_name
        student.gender = gender if gender else None
        student.date_of_birth = date_of_birth
        student.email = email if email else None
        student.phone = phone if phone else None
        student.course = course if course else None
        student.department = department
        student.semester = semester

        db.session.commit()

        flash('Student Updated Successfully', 'success')
        return redirect(url_for('students.index'))

    return render_template('students/form.html', student=student, action='Edit')


@students_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    """
    Delete student record from database.
    """
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    flash('Student Deleted Successfully', 'success')
    return redirect(url_for('students.index'))
