"""
tests/test_marks.py
==============================================================================
Project: College Student Performance Analytics System
Description: Unit tests for Marks Management Blueprint (CRUD, validations,
             summary metrics, search filtering).
==============================================================================
"""

import unittest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.student import Student
from app.models.subject import Subject
from app.models.marks import Marks


class MarksTestCase(unittest.TestCase):
    """Test case for Marks Management module."""

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

            # Create sample marks record (Internal: 25, External: 55, Total: 80)
            marks = Marks(
                student_id=student.id,
                subject_id=subject.id,
                internal_marks=25.0,
                external_marks=55.0
            )
            db.session.add(marks)
            db.session.commit()

            self.student_id = student.id
            self.subject_id = subject.id
            self.marks_id = marks.id

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

    def test_marks_overview_loads(self):
        """Verify marks overview list and summary cards load successfully."""
        response = self.client.get('/marks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Marks Management", response.data)
        self.assertIn(b"Alice Johnson", response.data)
        self.assertIn(b"80.0", response.data)  # Calculated total
        self.assertIn(b"Average Marks", response.data)
        self.assertIn(b"Highest Marks", response.data)

    def test_add_marks_success(self):
        """Verify adding new marks record calculates total and saves record."""
        # Create second subject first
        with self.app.app_context():
            sub2 = Subject(subject_code='CS502', subject_name='Web Tech', semester=5)
            db.session.add(sub2)
            db.session.commit()
            sub2_id = sub2.id

        response = self.client.post('/marks/add', data={
            'student_id': str(self.student_id),
            'subject_id': str(sub2_id),
            'internal_marks': '28.0',
            'external_marks': '62.0'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Marks saved successfully.", response.data)

        with self.app.app_context():
            rec = Marks.query.filter_by(subject_id=sub2_id).first()
            self.assertIsNotNone(rec)
            self.assertEqual(rec.internal_marks + rec.external_marks, 90.0)

    def test_add_marks_invalid_internal_rejected(self):
        """Verify internal marks outside range 0-30 are rejected."""
        response = self.client.post('/marks/add', data={
            'student_id': str(self.student_id),
            'subject_id': str(self.subject_id),
            'internal_marks': '35.0',  # Exceeds max 30
            'external_marks': '50.0'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Internal Marks must be between 0 and 30.", response.data)

    def test_add_marks_invalid_external_rejected(self):
        """Verify external marks outside range 0-70 are rejected."""
        response = self.client.post('/marks/add', data={
            'student_id': str(self.student_id),
            'subject_id': str(self.subject_id),
            'internal_marks': '20.0',
            'external_marks': '75.0'  # Exceeds max 70
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"External Marks must be between 0 and 70.", response.data)

    def test_add_marks_duplicate_rejected(self):
        """Verify duplicate marks record for same student and subject is rejected."""
        response = self.client.post('/marks/add', data={
            'student_id': str(self.student_id),
            'subject_id': str(self.subject_id),  # Existing subject from setUp
            'internal_marks': '20.0',
            'external_marks': '50.0'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Marks record already exists for this student and subject.", response.data)

    def test_edit_marks_success(self):
        """Verify editing marks record updates internal and external scores."""
        response = self.client.post(f'/marks/edit/{self.marks_id}', data={
            'student_id': str(self.student_id),
            'subject_id': str(self.subject_id),
            'internal_marks': '30.0',
            'external_marks': '68.0'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Marks updated successfully.", response.data)

        with self.app.app_context():
            rec = Marks.query.get(self.marks_id)
            self.assertEqual(rec.internal_marks, 30.0)
            self.assertEqual(rec.external_marks, 68.0)

    def test_delete_marks_success(self):
        """Verify deleting marks record removes it from database."""
        response = self.client.post(f'/marks/delete/{self.marks_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Marks deleted successfully.", response.data)

        with self.app.app_context():
            rec = Marks.query.get(self.marks_id)
            self.assertIsNone(rec)


if __name__ == '__main__':
    unittest.main()
