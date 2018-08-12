# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'sqlite:///catalog_items.db'
DATABASE_CONNECT_OPTIONS = {}

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True