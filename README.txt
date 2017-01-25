# First, start a virtual environment
virtualenv venv                     # If not already created
source venv/bin/activate            # Activate the virtual environment

# To install everything this app needs, run:
pip install --editable .
# This goes and reads the setup.py file (I think) and installs all necessary packages.
# This isn't working how I'd like; you have to pip install all your packages during development?

# Then run
export FLASK_APP=<app_name>         # This allows you to start the app with 'flask run'
export FLASK_DEBUG=true             # If you want to debug flask
flask run                           # Start flask

# Of course, don't forget to quit the virtual environment
decativate
