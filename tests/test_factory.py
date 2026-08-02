"""
tests/test_factory.py
==============================================================================
Project: College Student Performance Analytics System
Description: Unit tests for verifying Application Factory creation, test config,
             and blueprint route responsiveness.
==============================================================================
"""

import unittest
from app import create_app


class FactoryTestCase(unittest.TestCase):
    """Test suite for Flask Application Factory and blueprint routes."""

    def setUp(self):
        """Set up test application and client before each test."""
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_config(self):
        """Verify testing configuration loading."""
        self.assertTrue(self.app.testing)

    def test_index_page(self):
        """Test main home page route returns HTTP 200 and project title string."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"College Student Performance Analytics System", response.data)

    def test_auth_login_page(self):
        """Test login route returns HTTP 200."""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)

    def test_protected_routes_redirect_unauthenticated(self):
        """Test protected routes redirect to login for unauthenticated users."""
        protected_routes = [
            '/analytics/',
            '/analytics/dashboard'
        ]
        for route in protected_routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 302)
                self.assertIn('/auth/login', response.location)


if __name__ == '__main__':
    unittest.main()
