"""
tests/test_attendance.py
==============================================================================
Project: College Student Performance Analytics System
Description: Unit tests for Attendance Management Blueprint (CRUD, metrics,
             search filtering, duplicate validation).
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


class AttendanceTestCase(unittest.TestCase):
    """Test case for Attendance Management module."""

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
            student = Student(
                roll_number='CS101',
                first_name='Alice',
                last_name='Johnson',
                department='Computer Engineering',
                semester=5
            )
            subject = Subject(
                subject_code='CS501',
                subject_name='Database Systems',
                semester=5
            )
            db.session.add_all([student, subject])
            db.session.commit()

            # Create sample attendance record
            attendance = Attendance(
                student_id=student.id,
                subject_id=subject.id,
                attendance_date=date(2026, 8, 1),
                status='Present'
            )
            db.session.add(attendance)
            db.session.commit()

            self.student_id = student.id
            self.subject_id = subject.id
            self.attendance_id = attendance.id

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

    def test_attendance_overview_loads(self):
        """Verify attendance list and summary metrics load successfully."""
        response = self.client.get('/attendance/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Attendance Management", response.data)
        self.assertIn(b"Alice Johnson", response.data)
        self.assertIn(b"Database Systems", response.data)
        self.assertIn(b"100.0%", response.data)

    def test_mark_attendance_success(self):
        """Verify marking attendance saves record and flashes success message."""
        response = self.client.post('/attendance/mark', data={
            'student_id': str(self.student_id),
            'subject_id': str(self.subject_id),
            'attendance_date': '2026-08-02',
            'status': 'Absent'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Attendance Saved Successfully", response.data)

        with self.app.app_context():
            rec = Attendance.query.filter_by(attendance_date=date(2026, 8, 2)).first()
            self.assertIsNotNone(rec)
            self.assertEqual(rec.status, 'Absent')

    def test_mark_attendance_duplicate_rejected(self):
        """Verify marking attendance for same student, subject, and date is rejected."""
        response = self.client.post('/attendance/mark', data={
            'student_id': str(self.student_id),
            'subject_id': str(self.subject_id),
            'attendance_date': '2026-08-01',  # Existing date from setUp
            'status': 'Present'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Attendance record already exists for this student, subject, and date.", response.data)

    def test_edit_attendance_success(self):
        """Verify editing attendance record updates data."""
        response = self.client.post(f'/attendance/edit/{self.attendance_id}', data={
            'student_id': str(self.student_id),
            'subject_id': str(self.subject_id),
            'attendance_date': '2026-08-01',
            'status': 'Absent'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Attendance Updated Successfully", response.data)

        with self.app.app_context():
            rec = Attendance.query.get(self.attendance_id)
            self.assertEqual(rec.status, 'Absent')

    def test_delete_attendance_success(self):
        """Verify deleting attendance record removes it from database."""
        response = self.client.post(f'/attendance/delete/{self.attendance_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Attendance Deleted Successfully", response.data)

        with self.app.app_context():
            rec = Attendance.query.get(self.attendance_id)
            self.assertIsNone(rec)


if __name__ == '__main__':
    unittest.main()
