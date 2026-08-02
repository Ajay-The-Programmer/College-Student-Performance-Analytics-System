"""
tests/test_students.py
==============================================================================
Project: College Student Performance Analytics System
Description: Unit tests for Student Management Blueprint (CRUD, validations,
             search filtering, pagination).
==============================================================================
"""

import unittest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.student import Student


class StudentTestCase(unittest.TestCase):
    """Test suite for Student Management CRUD functionality."""

    def setUp(self):
        """Set up test application, in-memory DB, and authenticated session."""
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create test user and log in
            user = User(username='faculty1', email='faculty1@college.edu', role='faculty')
            user.set_password('password123')
            db.session.add(user)

            # Create sample students
            student1 = Student(
                roll_number='CS101',
                first_name='Alice',
                last_name='Johnson',
                department='Computer Engineering',
                semester=5,
                email='alice@college.edu',
                course='B.Tech'
            )
            student2 = Student(
                roll_number='CS102',
                first_name='Bob',
                last_name='Smith',
                department='Information Tech',
                semester=3,
                email='bob@college.edu',
                course='Diploma CS'
            )
            db.session.add_all([student1, student2])
            db.session.commit()

        # Log in test client
        self.client.post('/auth/login', data={
            'username': 'faculty1',
            'password': 'password123'
        })

    def tearDown(self):
        """Clean up database after tests."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_student_list_loads(self):
        """Verify student list page displays student records."""
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CS101", response.data)
        self.assertIn(b"Alice Johnson", response.data)
        self.assertIn(b"CS102", response.data)

    def test_student_search(self):
        """Verify searching student list filters results."""
        response = self.client.get('/students/?q=Alice')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CS101", response.data)
        self.assertNotIn(b"CS102", response.data)

    def test_add_student_success(self):
        """Verify adding a new student saves record and flashes success message."""
        response = self.client.post('/students/add', data={
            'roll_number': 'CS103',
            'first_name': 'Charlie',
            'last_name': 'Brown',
            'gender': 'Male',
            'date_of_birth': '2002-05-15',
            'email': 'charlie@college.edu',
            'phone': '9876543210',
            'course': 'Diploma CS',
            'department': 'Computer Engineering',
            'semester': '4'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student added successfully.", response.data)
        self.assertIn(b"CS103", response.data)

    def test_add_student_duplicate_roll_number(self):
        """Verify duplicate roll number is rejected."""
        response = self.client.post('/students/add', data={
            'roll_number': 'CS101',  # Existing roll number
            'first_name': 'Dave',
            'last_name': 'Miller',
            'department': 'Computer Engineering',
            'semester': '2'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Roll Number already exists.", response.data)

    def test_add_student_invalid_semester(self):
        """Verify semester outside range 1-8 is rejected."""
        response = self.client.post('/students/add', data={
            'roll_number': 'CS104',
            'first_name': 'Eve',
            'last_name': 'Davis',
            'department': 'Electronics',
            'semester': '9'  # Invalid semester > 8
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Semester must be an integer between 1 and 8.", response.data)

    def test_edit_student_success(self):
        """Verify editing student updates record and flashes success message."""
        with self.app.app_context():
            student = Student.query.filter_by(roll_number='CS101').first()
            student_id = student.id

        response = self.client.post(f'/students/edit/{student_id}', data={
            'roll_number': 'CS101',
            'first_name': 'Alice',
            'last_name': 'Williams',  # Updated last name
            'department': 'Computer Engineering',
            'semester': '6'  # Updated semester
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student updated successfully.", response.data)
        self.assertIn(b"Alice Williams", response.data)

    def test_delete_student_success(self):
        """Verify deleting student removes record and flashes success message."""
        with self.app.app_context():
            student = Student.query.filter_by(roll_number='CS102').first()
            student_id = student.id

        response = self.client.post(f'/students/delete/{student_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student deleted successfully.", response.data)

        with self.app.app_context():
            deleted_student = Student.query.get(student_id)
            self.assertIsNone(deleted_student)


if __name__ == '__main__':
    unittest.main()
