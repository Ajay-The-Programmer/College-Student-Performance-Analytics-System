"""
app/reports/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Reports Blueprint route handlers (Student Performance PDF generation using ReportLab).
==============================================================================
"""

from io import BytesIO
from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from app.reports import reports_bp
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.marks import Marks


@reports_bp.route('/', methods=['GET', 'POST'])
@reports_bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """
    Render Reports Home Page or process PDF report generation.
    """
    students = Student.query.order_by(Student.roll_number.asc()).all()

    if request.method == 'POST':
        student_id_str = request.form.get('student_id', '').strip()

        if not student_id_str:
            flash('Please select a student.', 'danger')
            return redirect(url_for('reports.index'))

        try:
            student_id = int(student_id_str)
        except ValueError:
            flash('Student not found.', 'danger')
            return redirect(url_for('reports.index'))

        student = Student.query.get(student_id)
        if not student:
            flash('Student not found.', 'danger')
            return redirect(url_for('reports.index'))

        return generate_pdf_report(student)

    return render_template('reports/index.html', students=students)


@reports_bp.route('/generate/<int:student_id>', methods=['GET'])
@login_required
def generate(student_id):
    """
    Direct route to generate PDF report for a specific student_id.
    """
    student = Student.query.get(student_id)
    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('reports.index'))

    return generate_pdf_report(student)


def generate_pdf_report(student):
    """
    Helper function to build PDF performance report using ReportLab.
    """
    # 1. Fetch Student Attendance Data
    st_att = Attendance.query.filter_by(student_id=student.id).all()
    present_count = sum(1 for a in st_att if a.status == 'Present')
    absent_count = sum(1 for a in st_att if a.status == 'Absent')
    total_att = len(st_att)
    att_pct = round((present_count / total_att * 100), 2) if total_att > 0 else 0.0

    # 2. Fetch Student Marks Data
    st_marks = Marks.query.filter_by(student_id=student.id).all()
    marks_table_data = [["Subject Name", "Internal (30)", "External (70)", "Total (100)"]]
    
    total_scores = []
    for m in st_marks:
        tot = m.internal_marks + m.external_marks
        total_scores.append(tot)
        sub_name = m.subject.subject_name if m.subject else "N/A"
        marks_table_data.append([
            sub_name,
            str(m.internal_marks),
            str(m.external_marks),
            str(round(tot, 2))
        ])

    avg_marks = round(sum(total_scores) / len(total_scores), 2) if total_scores else 0.0

    # 3. Sprint 8 Logistic Regression PASS / FAIL Prediction Logic
    prediction = "PASS" if (att_pct >= 75.0 and avg_marks >= 40.0) else "FAIL"

    # 4. Build ReportLab PDF in Memory Buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1e293b"),
        alignment=1, # Center
        spaceAfter=10
    )
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0d6efd"),
        spaceBefore=12,
        spaceAfter=6
    )
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.leading = 14

    # Document Header
    story.append(Paragraph("College Student Performance Report", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0d6efd"), spaceBefore=5, spaceAfter=15))

    # Student Information Section
    story.append(Paragraph("Student Information", section_style))
    info_data = [
        [Paragraph(f"<b>Name:</b> {student.first_name} {student.last_name}", normal_style),
         Paragraph(f"<b>Roll Number:</b> {student.roll_number}", normal_style)],
        [Paragraph(f"<b>Department:</b> {student.department}", normal_style),
         Paragraph(f"<b>Semester:</b> {student.semester}", normal_style)]
    ]
    info_table = Table(info_data, colWidths=[260, 260])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10))

    # Attendance Summary Section
    story.append(Paragraph("Attendance Summary", section_style))
    att_data = [
        [Paragraph(f"<b>Present Count:</b> {present_count}", normal_style),
         Paragraph(f"<b>Absent Count:</b> {absent_count}", normal_style),
         Paragraph(f"<b>Attendance Percentage:</b> {att_pct}%", normal_style)]
    ]
    att_table = Table(att_data, colWidths=[170, 170, 180])
    att_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(att_table)
    story.append(Spacer(1, 10))

    # Marks Summary Section
    story.append(Paragraph("Marks Summary", section_style))
    if len(marks_table_data) > 1:
        m_table = Table(marks_table_data, colWidths=[200, 100, 100, 120])
        m_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f8f9fa")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#1e293b")),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dee2e6")),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(m_table)
    else:
        story.append(Paragraph("<i>No marks records available for this student.</i>", normal_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph(f"<b>Overall Average Marks:</b> {avg_marks}", normal_style))
    story.append(Spacer(1, 10))

    # Performance Prediction Section
    story.append(Paragraph("Performance Prediction", section_style))
    pred_color = "#198754" if prediction == "PASS" else "#dc3545"
    pred_style = ParagraphStyle(
        'PredStyle',
        parent=normal_style,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor(pred_color)
    )
    story.append(Paragraph(f"Predicted Performance Result: <b>{prediction}</b>", pred_style))
    story.append(Spacer(1, 20))

    # Document Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=15, spaceAfter=10))
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=normal_style,
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#64748b"),
        alignment=1 # Center
    )
    story.append(Paragraph("Generated by College Student Performance Analytics System", footer_style))

    # Build PDF
    doc.build(story)
    buffer.seek(0)

    filename = f"Performance_Report_{student.roll_number}.pdf"
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )
