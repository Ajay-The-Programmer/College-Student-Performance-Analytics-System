"""
app/marks/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Marks Management Blueprint route handlers (Overview, Add, Edit, Delete).
==============================================================================
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.marks import marks_bp
from app.extensions import db
from app.models.marks import Marks
from app.models.student import Student
from app.models.subject import Subject


@marks_bp.route('/')
@marks_bp.route('/overview')
@login_required
def overview():
    """
    Render Academic Marks Overview, Summary Cards, and Paginated Records List.
    """
    search_query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)

    query = Marks.query.join(Student).join(Subject)

    if search_query:
        query = query.filter(
            (Student.first_name.ilike(f"%{search_query}%")) |
            (Student.last_name.ilike(f"%{search_query}%")) |
            (Student.roll_number.ilike(f"%{search_query}%")) |
            (Subject.subject_name.ilike(f"%{search_query}%")) |
            (Subject.subject_code.ilike(f"%{search_query}%"))
        )

    pagination = query.order_by(Marks.id.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    marks_list = pagination.items

    # Summary Metrics Calculations
    total_records = Marks.query.count()
    all_marks = Marks.query.all()

    if all_marks:
        totals = [m.internal_marks + m.external_marks for m in all_marks]
        avg_marks = round(sum(totals) / len(totals), 2)
        highest_marks = round(max(totals), 2)
    else:
        avg_marks = 0.0
        highest_marks = 0.0

    return render_template(
        'marks/overview.html',
        marks_list=marks_list,
        pagination=pagination,
        search_query=search_query,
        total_records=total_records,
        avg_marks=avg_marks,
        highest_marks=highest_marks
    )


@marks_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_marks():
    """
    Add new marks record for a student and subject.
    """
    students = Student.query.order_by(Student.roll_number.asc()).all()
    subjects = Subject.query.order_by(Subject.subject_code.asc()).all()

    if request.method == 'POST':
        student_id_str = request.form.get('student_id', '').strip()
        subject_id_str = request.form.get('subject_id', '').strip()
        internal_str = request.form.get('internal_marks', '').strip()
        external_str = request.form.get('external_marks', '').strip()

        errors = []

        if not student_id_str:
            errors.append('Student selection is required.')
        if not subject_id_str:
            errors.append('Subject selection is required.')

        student_id = None
        subject_id = None
        internal_marks = None
        external_marks = None

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

        # Internal Marks Validation (0 to 30)
        if not internal_str:
            errors.append('Internal Marks are required.')
        else:
            try:
                internal_marks = float(internal_str)
                if internal_marks < 0 or internal_marks > 30:
                    errors.append('Internal Marks must be between 0 and 30.')
            except ValueError:
                errors.append('Internal Marks must be a valid number between 0 and 30.')

        # External Marks Validation (0 to 70)
        if not external_str:
            errors.append('External Marks are required.')
        else:
            try:
                external_marks = float(external_str)
                if external_marks < 0 or external_marks > 70:
                    errors.append('External Marks must be between 0 and 70.')
            except ValueError:
                errors.append('External Marks must be a valid number between 0 and 70.')

        # Prevent duplicate record for same student and subject
        if student_id and subject_id:
            existing = Marks.query.filter_by(
                student_id=student_id,
                subject_id=subject_id
            ).first()
            if existing:
                errors.append('Marks record already exists for this student and subject.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template(
                'marks/form.html',
                students=students,
                subjects=subjects,
                marks=request.form,
                action='Add'
            )

        # Create and save new marks record
        new_marks = Marks(
            student_id=student_id,
            subject_id=subject_id,
            internal_marks=internal_marks,
            external_marks=external_marks
        )

        db.session.add(new_marks)
        db.session.commit()

        flash('Marks saved successfully.', 'success')
        return redirect(url_for('marks.overview'))

    return render_template(
        'marks/form.html',
        students=students,
        subjects=subjects,
        marks=None,
        action='Add'
    )


@marks_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_marks(id):
    """
    Edit existing marks record.
    """
    marks = Marks.query.get_or_404(id)
    students = Student.query.order_by(Student.roll_number.asc()).all()
    subjects = Subject.query.order_by(Subject.subject_code.asc()).all()

    if request.method == 'POST':
        student_id_str = request.form.get('student_id', '').strip()
        subject_id_str = request.form.get('subject_id', '').strip()
        internal_str = request.form.get('internal_marks', '').strip()
        external_str = request.form.get('external_marks', '').strip()

        errors = []

        if not student_id_str:
            errors.append('Student selection is required.')
        if not subject_id_str:
            errors.append('Subject selection is required.')

        student_id = None
        subject_id = None
        internal_marks = None
        external_marks = None

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

        if not internal_str:
            errors.append('Internal Marks are required.')
        else:
            try:
                internal_marks = float(internal_str)
                if internal_marks < 0 or internal_marks > 30:
                    errors.append('Internal Marks must be between 0 and 30.')
            except ValueError:
                errors.append('Internal Marks must be a valid number between 0 and 30.')

        if not external_str:
            errors.append('External Marks are required.')
        else:
            try:
                external_marks = float(external_str)
                if external_marks < 0 or external_marks > 70:
                    errors.append('External Marks must be between 0 and 70.')
            except ValueError:
                errors.append('External Marks must be a valid number between 0 and 70.')

        if student_id and subject_id:
            existing = Marks.query.filter(
                Marks.student_id == student_id,
                Marks.subject_id == subject_id,
                Marks.id != id
            ).first()
            if existing:
                errors.append('Marks record already exists for this student and subject.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template(
                'marks/form.html',
                students=students,
                subjects=subjects,
                marks=marks,
                action='Edit'
            )

        # Update marks details
        marks.student_id = student_id
        marks.subject_id = subject_id
        marks.internal_marks = internal_marks
        marks.external_marks = external_marks

        db.session.commit()

        flash('Marks updated successfully.', 'success')
        return redirect(url_for('marks.overview'))

    return render_template(
        'marks/form.html',
        students=students,
        subjects=subjects,
        marks=marks,
        action='Edit'
    )


@marks_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_marks(id):
    """
    Delete marks record from database.
    """
    marks = Marks.query.get_or_404(id)
    db.session.delete(marks)
    db.session.commit()

    flash('Marks deleted successfully.', 'success')
    return redirect(url_for('marks.overview'))
