"""
app/admin/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Admin Blueprint route handlers (Dashboard, User Management, Settings).
==============================================================================
"""

from flask import render_template
from app.admin import admin_bp


@admin_bp.route('/')
@admin_bp.route('/dashboard')
def dashboard():
    """Render Admin Control Panel Dashboard."""
    return render_template('admin/dashboard.html')


@admin_bp.route('/users')
def users():
    """Render Admin User Management View."""
    return render_template('admin/users.html')


@admin_bp.route('/settings')
def settings():
    """Render System Settings View."""
    return render_template('admin/settings.html')
