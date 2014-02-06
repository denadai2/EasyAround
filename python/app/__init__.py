from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from collections import namedtuple

#---------------
# Classes and data structures
#---------------
Requirements = namedtuple("Requirements", "startDate days kids freeTime client")
Preferences = namedtuple("Preferences", "shopping culture gastronomy nightlife")
Constraints = namedtuple("Constraints", "exclude include")
Violation = namedtuple("Violation", "itineraryID clientID locations")

#---------------
# Application
#---------------
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)

from app import controllers, models