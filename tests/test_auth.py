"""
tests/test_auth.py
==============================================================================
Project: College Student Performance Analytics System
Description: Unit tests for verifying Authentication Blueprint (login/logout).
==============================================================================
"""

import unittest
from app import create_app
from app.extensions import db
from app.models.user import User


class AuthTestCase(unittest.TestCase):
    """Test case for Authentication module."""

    def setUp(self):
        """Set up test application and in-memory database context."""
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create test Admin user
            admin = User(username='admin', email='admin@college.edu', role='admin')
            admin.set_password('admin123')

            # Create test Faculty user
            faculty = User(username='faculty', email='faculty@college.edu', role='faculty')
            faculty.set_password('faculty123')

            db.session.add(admin)
            db.session.add(faculty)
            db.session.commit()

    def tearDown(self):
        """Clean up database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page_loads(self):
        """Verify GET /auth/login returns HTTP 200."""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User Login", response.data)

    def test_invalid_login(self):
        """Verify invalid login displays error message."""
        response = self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username or password.", response.data)

    def test_admin_login_redirects_to_dashboard(self):
        """Verify successful admin login redirects to common dashboard."""
        response = self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login Successful", response.data)

    def test_faculty_login_redirects_to_dashboard(self):
        """Verify successful faculty login redirects to common dashboard."""
        response = self.client.post('/auth/login', data={
            'username': 'faculty',
            'password': 'faculty123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login Successful", response.data)

    def test_logout(self):
        """Verify logout redirects to login page."""
        self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Logout Successful", response.data)


if __name__ == '__main__':
    unittest.main()
