import flask
from flask.ext.sqlalchemy import SQLAlchemy

__all__ = ['app', 'db']

app = flask.Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# Declare model classes here.
# This is not necessary, but by importing the module here,
# you can just only import `db` in anywhere.
import animeta.models

# Install views.
from animeta import views
views.init_app(app)
