#!flask/bin/python
from flask import Flask
from flask import jsonify
import sqlite3
from contextlib import closing
from itinerary import *
import json
import sys

app = Flask(__name__)

#---------------
# Classes and data structures
#---------------

Requirements = namedtuple("Requirements", "start days kids freeTime existingClient clientName clientDinamicity clientQuiet")
Preferences = namedtuple("Preferences", "shopping culture gastronomy nightlife")
Constraints = namedtuple("Constraints", "exclude include")

# Note: changed class name from "Requirements" to "Request" otherwise it will get messed up
class Request:
	''' Class that has to handle the methods operationalize and specify.'''
	req = None
	pref = None
	constr = None
	def operationalize(self, startDate, numberOfDays, presenceOfKids, needsFreeTime, exclude, include, existingClient, clientName, clientDinamicity, clientQuiet, preferenceShopping, preferenceCulture, preferenceGastronomy, preferenceNightLife):
		self.req = Requirements(startDate, numberOfDays, presenceOfKids, needsFreeTime, existingClient, clientName, clientDinamicity, clientQuiet)
		self.pref = Preferences(preferenceShopping, preferenceCulture, preferenceGastronomy, preferenceNightLife)
		self.constr = Constraints(exclude, include)
		return 0
	def specify(self):
		itinerary = Itinerary (self.req.start, self.req.days, self.req.existingClient)
		return itinerary 

#----------------
# Handler of the POST request 
#----------------	
@app.route('/hello', methods = ['POST'])
def getRequest():
	newReq = Request()
	newReq.operationalize(request.form['startDate'], request.form['numberOfDays'], request.form['presenceOfKids'], request.form['needsFreeTime'], request.form['exclude'], request.form['include'], request.form['existingClient'], request.form['clientName'], request.form['clientDinamicity'], request.form['clientQuiet'], request.form['preferenceShopping'], request.form['preferenceCulture'], request.form['preferenceGastronomy'], request.form['preferenceNightLife'])
	itinerary = newReq.specify()
	return itinerary


if __name__ == '__main__':
    app.run(debug = True)

