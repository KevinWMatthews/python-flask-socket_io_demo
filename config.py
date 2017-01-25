# This affects python run.py but does not affect 'flask run'.
# To change the settings for 'flask run', run 'export FLASK_DEBUG=true' from the console.
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
