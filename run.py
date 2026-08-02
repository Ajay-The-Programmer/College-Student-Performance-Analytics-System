"""
run.py
==============================================================================
Project: College Student Performance Analytics System
Description: Entry point script for executing the Flask web application.
             Instantiates the Flask app using the Application Factory pattern.
==============================================================================
"""

import os
from app import create_app

# Fetch environment setting or fallback to default 'development'
config_name = os.getenv('FLASK_ENV', 'development')

# Create Flask application instance via Application Factory
app = create_app(config_name)

if __name__ == '__main__':
    # Launch local development server
    # Port defaults to 5000, host to localhost
    app.run(
        host=os.getenv('FLASK_RUN_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_RUN_PORT', 5000)),
        debug=app.config.get('DEBUG', True)
    )
