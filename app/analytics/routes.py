"""
app/analytics/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Analytics Blueprint route handlers (Summary Cards, Plotly Charts,
             At-Risk Student Identification).
==============================================================================
"""

import json
from flask import render_template
from flask_login import login_required
import plotly
import plotly.express as px

from app.analytics import analytics_bp
from app.models.student import Student
from app.models.subject import Subject
from app.models.attendance import Attendance
from app.models.marks import Marks


@analytics_bp.route('/')
@analytics_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Render Analytics Dashboard with Summary Cards, Plotly Charts, and At Risk Students Table.
    """
    # 1. Summary Cards Metrics
    total_students = Student.query.count()
    total_subjects = Subject.query.count()

    total_att_records = Attendance.query.count()
    total_present = Attendance.query.filter_by(status='Present').count()
    total_absent = Attendance.query.filter_by(status='Absent').count()
    avg_attendance_pct = round((total_present / total_att_records * 100), 2) if total_att_records > 0 else 0.0

    all_marks = Marks.query.all()
    if all_marks:
        totals = [m.internal_marks + m.external_marks for m in all_marks]
        avg_marks = round(sum(totals) / len(totals), 2)
    else:
        avg_marks = 0.0

    # 2. At Risk Students Logic & Table
    students = Student.query.order_by(Student.roll_number.asc()).all()
    at_risk_students_list = []
    student_names_bar = []
    student_scores_bar = []

    for s in students:
        # Attendance % for student
        st_att = Attendance.query.filter_by(student_id=s.id).all()
        if st_att:
            st_present = sum(1 for a in st_att if a.status == 'Present')
            att_pct = round((st_present / len(st_att)) * 100, 2)
        else:
            att_pct = None

        # Average marks for student
        st_marks = Marks.query.filter_by(student_id=s.id).all()
        if st_marks:
            st_totals = [m.internal_marks + m.external_marks for m in st_marks]
            st_avg_marks = round(sum(st_totals) / len(st_totals), 2)
        else:
            st_avg_marks = None

        # Populate bar chart data if student has marks
        if st_avg_marks is not None:
            student_names_bar.append(f"{s.first_name} {s.last_name}")
            student_scores_bar.append(st_avg_marks)

        # Determine At-Risk Status (Attendance < 75% OR Total Marks < 40)
        is_low_att = (att_pct is not None and att_pct < 75.0)
        is_low_marks = (st_avg_marks is not None and st_avg_marks < 40.0)

        if is_low_att or is_low_marks:
            if is_low_att and is_low_marks:
                reason = "Both"
            elif is_low_att:
                reason = "Low Attendance"
            else:
                reason = "Low Marks"

            at_risk_students_list.append({
                'roll_number': s.roll_number,
                'name': f"{s.first_name} {s.last_name}",
                'attendance_pct': f"{att_pct}%" if att_pct is not None else "N/A",
                'avg_marks': st_avg_marks if st_avg_marks is not None else "N/A",
                'reason': reason
            })

    total_at_risk = len(at_risk_students_list)

    # 3. Plotly Chart 1: Attendance Distribution (Pie Chart)
    fig1 = px.pie(
        names=['Present', 'Absent'],
        values=[total_present, total_absent] if (total_present + total_absent) > 0 else [1, 0],
        title='Attendance Distribution (Present vs Absent)',
        color=['Present', 'Absent'],
        color_discrete_map={'Present': '#198754', 'Absent': '#dc3545'}
    )
    fig1.update_layout(
        margin=dict(t=40, b=20, l=20, r=20),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#1e293b")
    )
    chart1_json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # 4. Plotly Chart 2: Student Marks (Bar Chart using Bootstrap theme palette)
    if not student_names_bar:
        student_names_bar = ['No Data']
        student_scores_bar = [0]
        bar_colors = ['#6c757d']
    else:
        # Dynamic Bootstrap palette based on score benchmarks
        bar_colors = [
            '#198754' if score >= 75 else ('#0d6efd' if score >= 40 else '#dc3545')
            for score in student_scores_bar
        ]

    fig2 = px.bar(
        x=student_names_bar,
        y=student_scores_bar,
        labels={'x': 'Student Name', 'y': 'Average Total Marks'},
        title='Student Marks Overview (Total Marks per Student)'
    )
    fig2.update_traces(
        marker_color=bar_colors,
        marker_line_color='#ffffff',
        marker_line_width=1.5,
        opacity=0.9
    )
    fig2.update_layout(
        margin=dict(t=40, b=20, l=20, r=20),
        height=350,
        yaxis=dict(range=[0, 100], gridcolor='#e9ecef'),
        xaxis=dict(gridcolor='#e9ecef'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#1e293b")
    )
    chart2_json = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        'analytics/dashboard.html',
        total_students=total_students,
        total_subjects=total_subjects,
        avg_attendance_pct=avg_attendance_pct,
        avg_marks=avg_marks,
        total_at_risk=total_at_risk,
        at_risk_students=at_risk_students_list,
        chart1_json=chart1_json,
        chart2_json=chart2_json
    )


@analytics_bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict_performance():
    """Placeholder route redirecting to dashboard."""
    return render_template('analytics/dashboard.html')


@analytics_bp.route('/at-risk')
@login_required
def at_risk_students():
    """Placeholder route redirecting to dashboard."""
    return render_template('analytics/dashboard.html')
