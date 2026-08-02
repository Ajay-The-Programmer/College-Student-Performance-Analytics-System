"""
app/attendance/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Attendance Blueprint route handlers (Overview, Mark Attendance, Edit, Delete, Metrics).
==============================================================================
"""

from datetime import datetime, date
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.attendance import attendance_bp
from app.extensions import db
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.subject import Subject


@attendance_bp.route('/')
@attendance_bp.route('/overview')
@login_required
def overview():
    """
    Render Attendance Overview, Summary Metrics, and Paginated Records List.
    """
    search_query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)

    query = Attendance.query.join(Student).join(Subject)

    if search_query:
        query = query.filter(
            (Student.first_name.ilike(f"%{search_query}%")) |
            (Student.last_name.ilike(f"%{search_query}%")) |
            (Student.roll_number.ilike(f"%{search_query}%")) |
            (Subject.subject_name.ilike(f"%{search_query}%")) |
            (Subject.subject_code.ilike(f"%{search_query}%"))
        )

    pagination = query.order_by(Attendance.attendance_date.desc(), Attendance.id.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    attendances = pagination.items

    # Attendance Summary Metrics
    total_records = Attendance.query.count()
    total_present = Attendance.query.filter_by(status='Present').count()
    total_absent = Attendance.query.filter_by(status='Absent').count()
    attendance_percentage = round((total_present / total_records * 100), 2) if total_records > 0 else 0.0

    return render_template(
        'attendance/overview.html',
        attendances=attendances,
        pagination=pagination,
        search_query=search_query,
        total_records=total_records,
        total_present=total_present,
        total_absent=total_absent,
        attendance_percentage=attendance_percentage
    )


@attendance_bp.route('/mark', methods=['GET', 'POST'])
@attendance_bp.route('/add', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    """
    Mark new attendance record for a student and subject.
    """
    students = Student.query.order_by(Student.roll_number.asc()).all()
    subjects = Subject.query.order_by(Subject.subject_code.asc()).all()

    if request.method == 'POST':
        student_id_str = request.form.get('student_id', '').strip()
        subject_id_str = request.form.get('subject_id', '').strip()
        date_str = request.form.get('attendance_date', '').strip()
        status = request.form.get('status', '').strip()

        errors = []

        if not student_id_str:
            errors.append('Student selection is required.')
        if not subject_id_str:
            errors.append('Subject selection is required.')
        if not date_str:
            errors.append('Attendance date is required.')
        if not status or status not in ['Present', 'Absent']:
            errors.append('Valid status (Present or Absent) is required.')

        student_id = None
        subject_id = None
        attendance_date = None

        if student_id_str:
            try:
                student_id = int(student_id_str)
            except ValueError:
                errors.append('Invalid student selected.')

        if subject_id_str:
            try:
                subject_id = int(subject_id_str)
            except ValueError:
                errors.append('Invalid subject selected.')

        if date_str:
            try:
                attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Invalid date format.')

        # Prevent duplicate attendance for same student, subject, and date
        if student_id and subject_id and attendance_date:
            existing = Attendance.query.filter_by(
                student_id=student_id,
                subject_id=subject_id,
                attendance_date=attendance_date
            ).first()
            if existing:
                errors.append('Attendance record already exists for this student, subject, and date.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template(
                'attendance/form.html',
                students=students,
                subjects=subjects,
                attendance=request.form,
                action='Mark'
            )

        # Create and save new attendance record
        new_attendance = Attendance(
            student_id=student_id,
            subject_id=subject_id,
            attendance_date=attendance_date,
            status=status
        )

        db.session.add(new_attendance)
        db.session.commit()

        flash('Attendance saved successfully.', 'success')
        return redirect(url_for('attendance.overview'))

    return render_template(
        'attendance/form.html',
        students=students,
        subjects=subjects,
        attendance=None,
        action='Mark'
    )


@attendance_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_attendance(id):
    """
    Edit existing attendance record.
    """
    attendance = Attendance.query.get_or_404(id)
    students = Student.query.order_by(Student.roll_number.asc()).all()
    subjects = Subject.query.order_by(Subject.subject_code.asc()).all()

    if request.method == 'POST':
        student_id_str = request.form.get('student_id', '').strip()
        subject_id_str = request.form.get('subject_id', '').strip()
        date_str = request.form.get('attendance_date', '').strip()
        status = request.form.get('status', '').strip()

        errors = []

        if not student_id_str:
            errors.append('Student selection is required.')
        if not subject_id_str:
            errors.append('Subject selection is required.')
        if not date_str:
            errors.append('Attendance date is required.')
        if not status or status not in ['Present', 'Absent']:
            errors.append('Valid status (Present or Absent) is required.')

        student_id = None
        subject_id = None
        attendance_date = None

        if student_id_str:
            try:
                student_id = int(student_id_str)
            except ValueError:
                errors.append('Invalid student selected.')

        if subject_id_str:
            try:
                subject_id = int(subject_id_str)
            except ValueError:
                errors.append('Invalid subject selected.')

        if date_str:
            try:
                attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Invalid date format.')

        if student_id and subject_id and attendance_date:
            existing = Attendance.query.filter(
                Attendance.student_id == student_id,
                Attendance.subject_id == subject_id,
                Attendance.attendance_date == attendance_date,
                Attendance.id != id
            ).first()
            if existing:
                errors.append('Attendance record already exists for this student, subject, and date.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template(
                'attendance/form.html',
                students=students,
                subjects=subjects,
                attendance=attendance,
                action='Edit'
            )

        # Update attendance details
        attendance.student_id = student_id
        attendance.subject_id = subject_id
        attendance.attendance_date = attendance_date
        attendance.status = status

        db.session.commit()

        flash('Attendance updated successfully.', 'success')
        return redirect(url_for('attendance.overview'))

    return render_template(
        'attendance/form.html',
        students=students,
        subjects=subjects,
        attendance=attendance,
        action='Edit'
    )


@attendance_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_attendance(id):
    """
    Delete attendance record from database.
    """
    attendance = Attendance.query.get_or_404(id)
    db.session.delete(attendance)
    db.session.commit()

    flash('Attendance deleted successfully.', 'success')
    return redirect(url_for('attendance.overview'))
