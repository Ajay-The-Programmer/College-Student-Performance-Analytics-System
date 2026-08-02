"""
tests/test_analytics.py
==============================================================================
Project: College Student Performance Analytics System
Description: Unit tests for Analytics Dashboard Blueprint (Summary Cards,
             Plotly Charts, At-Risk Student Identification).
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


class AnalyticsTestCase(unittest.TestCase):
    """Test case for Analytics Dashboard module."""

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

            # Create sample students
            s1 = Student(roll_number='CS101', first_name='Alice', last_name='Johnson', department='CS', semester=5)
            s2 = Student(roll_number='CS102', first_name='Bob', last_name='Smith', department='CS', semester=5)
            db.session.add_all([s1, s2])

            # Create sample subject
            sub = Subject(subject_code='CS501', subject_name='Database Systems', semester=5)
            db.session.add(sub)
            db.session.commit()

            # Student 1: Good attendance, good marks
            att1 = Attendance(student_id=s1.id, subject_id=sub.id, attendance_date=date(2026, 8, 1), status='Present')
            marks1 = Marks(student_id=s1.id, subject_id=sub.id, internal_marks=25.0, external_marks=55.0)  # Total 80

            # Student 2: Low attendance (Absent), Low marks (Total 35) -> At Risk
            att2 = Attendance(student_id=s2.id, subject_id=sub.id, attendance_date=date(2026, 8, 1), status='Absent')
            marks2 = Marks(student_id=s2.id, subject_id=sub.id, internal_marks=10.0, external_marks=25.0)  # Total 35

            db.session.add_all([att1, marks1, att2, marks2])
            db.session.commit()

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

    def test_dashboard_loads(self):
        """Verify analytics dashboard renders summary cards and charts."""
        response = self.client.get('/analytics/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Analytics Dashboard", response.data)
        self.assertIn(b"Total Students", response.data)
        self.assertIn(b"Total Subjects", response.data)
        self.assertIn(b"Avg Attendance %", response.data)
        self.assertIn(b"Avg Marks", response.data)
        self.assertIn(b"Students At Risk", response.data)

    def test_at_risk_students_identification(self):
        """Verify student with low attendance and low marks is listed in At Risk table."""
        response = self.client.get('/analytics/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bob Smith", response.data)
        self.assertIn(b"CS102", response.data)
        self.assertIn(b"Both", response.data)


if __name__ == '__main__':
    unittest.main()
