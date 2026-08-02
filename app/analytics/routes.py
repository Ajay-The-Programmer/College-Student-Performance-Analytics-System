"""
app/analytics/routes.py
==============================================================================
Project: College Student Performance Analytics System
Description: Analytics Blueprint route handlers (Dashboard, Predictive ML Models,
             Plotly Interactive Visualizations, Risk Analysis).
==============================================================================
"""

from flask import render_template
from flask_login import login_required
from app.analytics import analytics_bp


@analytics_bp.route('/')
@analytics_bp.route('/dashboard')
@login_required
def dashboard():
    """Render Analytics Dashboard with interactive Plotly charts."""
    return render_template('analytics/dashboard.html')


@analytics_bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict_performance():
    """Render Student Performance Prediction Model interface."""
    return render_template('analytics/predict.html')


@analytics_bp.route('/at-risk')
@login_required
def at_risk_students():
    """Render At-Risk Student Identification view using Scikit-Learn classifiers."""
    return render_template('analytics/at_risk.html')
