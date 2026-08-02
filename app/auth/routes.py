"""
app/auth/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Authentication Blueprint route handlers for Admin and Faculty Login/Logout.
==============================================================================
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.models.user import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login route for Admin and Faculty accounts.
    Redirects both roles to the main dashboard after login.
    """
    # If user is already logged in, redirect to main dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Find user by username
        user = User.query.filter_by(username=username).first()

        # Validate user credentials
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Log out the current user and redirect to login page.
    """
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
