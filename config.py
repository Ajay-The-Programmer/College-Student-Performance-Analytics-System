"""
config.py
==============================================================================
Project: College Student Performance Analytics System
Description: Application configuration settings management.
==============================================================================
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Base Configuration Class containing common settings across all environments."""
    
    # Secret Key for signing session cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-fallback-secret-key-dev-only'
    
    # SQLAlchemy tracking configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MySQL Database Connection parameters with fallback defaults
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'college_student_analytics')

    # Construct MySQL SQLAlchemy Database URI
    DEFAULT_MYSQL_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DEFAULT_MYSQL_URI

    # Application level constants
    PAGINATION_PER_PAGE = 10
    ANALYTICS_MODEL_PATH = os.path.join(basedir, 'datasets')


class DevelopmentConfig(Config):
    """Development Environment Configuration."""
    DEBUG = True
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    """Testing Environment Configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production Environment Configuration."""
    DEBUG = False
    TESTING = False


# Configuration mapping dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
