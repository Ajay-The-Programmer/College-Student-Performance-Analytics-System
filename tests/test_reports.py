"""
tests/test_reports.py
==============================================================================
Project: College Student Performance Analytics System
Description: Unit tests for Reports Blueprint (PDF generation, validation,
             login authentication protection).
==============================================================================
"""

import unittest
from datetime import date
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.student import Student
from app.models.subject import Subject
from app.models.attendance import Attendance
from app.models.marks import Marks


class ReportsTestCase(unittest.TestCase):
    """Test case for Reports PDF generation module."""

    def setUp(self):
        """Set up test application, in-memory DB, test data, and user session."""
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create test user
            user = User(username='faculty1', email='faculty1@college.edu', role='faculty')
            user.set_password('password123')
            db.session.add(user)

            # Create sample student and subject
            student = Student(roll_number='CS101', first_name='Alice', last_name='Johnson', department='CS', semester=5)
            subject = Subject(subject_code='CS501', subject_name='Database Systems', semester=5)
            db.session.add_all([student, subject])
            db.session.commit()

            # Add sample attendance and marks
            att = Attendance(student_id=student.id, subject_id=subject.id, attendance_date=date(2026, 8, 1), status='Present')
            marks = Marks(student_id=student.id, subject_id=subject.id, internal_marks=25.0, external_marks=55.0)
            db.session.add_all([att, marks])
            db.session.commit()

            self.student_id = student.id

        # Log in test client
        self.client.post('/auth/login', data={
            'username': 'faculty1',
            'password': 'password123'
        })

    def tearDown(self):
        """Clean up database context after tests."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_reports_page_loads(self):
        """Verify Reports index page loads successfully."""
        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Generate Student Report", response.data)
        self.assertIn(b"CS101", response.data)

    def test_pdf_generation_success(self):
        """Verify PDF report generation returns PDF stream for valid student."""
        response = self.client.post('/reports/', data={
            'student_id': str(self.student_id)
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/pdf')
        self.assertTrue(response.data.startswith(b'%PDF'))

    def test_no_student_selected_handled(self):
        """Verify submitting without student flashes error message."""
        response = self.client.post('/reports/', data={
            'student_id': ''
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please select a student.", response.data)

    def test_invalid_student_handled(self):
        """Verify non-existent student ID flashes error message."""
        response = self.client.post('/reports/', data={
            'student_id': '99999'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student not found.", response.data)

    def test_login_required(self):
        """Verify reports route redirects unauthenticated users to login page."""
        # Log out
        self.client.get('/auth/logout')
        response = self.client.get('/reports/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User Login", response.data)


if __name__ == '__main__':
    unittest.main()
