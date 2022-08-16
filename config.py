import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
database_name = 'fyyurdb'
username = 'postgres'
password = '2022passdespostgres'
host_port = 'localhost:5432'
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
                            username,
                            password,
                            host_port,
                            database_name );
SQLALCHEMY_TRACK_MODIFICATIONS = False
