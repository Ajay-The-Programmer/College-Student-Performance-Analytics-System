"""
config.py
==============================================================================
Project: College Student Performance Analytics System
Description: Application configuration settings management utilizing class-based
             inheritance for different deployment environments (Development,
             Testing, Production). Loads variables securely from environment variables.
==============================================================================
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Base Configuration Class containing common settings across all environments."""
    
    # Secret Key for signing session cookies and CSRF tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-fallback-secret-key-dev-only'
    
    # SQLAlchemy tracking configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MySQL Database Connection parameters with fallback defaults
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'student_analytics_db')

    # Construct MySQL SQLAlchemy Database URI
    # Fallback to SQLite memory database if MySQL parameters are unconfigured
    DEFAULT_MYSQL_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DEFAULT_MYSQL_URI

    # Application level constants
    PAGINATION_PER_PAGE = 25
    ANALYTICS_MODEL_PATH = os.path.join(basedir, 'datasets')


class DevelopmentConfig(Config):
    """Development Environment Specific Configuration."""
    DEBUG = True
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    """Testing Environment Specific Configuration."""
    TESTING = True
    DEBUG = True
    # Use SQLite in-memory database for fast test execution
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production Environment Specific Configuration."""
    DEBUG = False
    TESTING = False
    # In production, ensure SECRET_KEY and DATABASE_URL are set via environment
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


# Configuration mapping dictionary for easy dynamic lookup
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
