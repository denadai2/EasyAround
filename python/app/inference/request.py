#!flask/bin/python
from flask import Flask
from flask import jsonify
import sqlite3
from contextlib import closing
from itinerary import *
import json

app = Flask(__name__)

#---------------
# Classes and data structures
#---------------

Requirements = namedtuple("Requirements", "startDate days kids freeTime existingClient clientName clientDinamicity clientQuiet")
Preferences = namedtuple("Preferences", "shopping culture gastronomy nightlife")
Constraints = namedtuple("Constraints", "exclude include")


# Note: changed class name from "Requirements" to "Request" otherwise it will get messed up
class Request:
	''' Class that has to handle the methods operationalize and specify.'''
	

	def operationalize(self, startDate, numberOfDays, presenceOfKids, needsFreeTime, exclude, include, client, 
		preferenceShopping, preferenceCulture, preferenceGastronomy, preferenceNightLife):
		"""Divides all the parameters in requirements, preferences and constraints.

	    Args:
	        startDate: date representing the start date of the trip
	        numberOfDays: number of trip days 
	        presenceOfKids: boolean representing if there are some kids in the trip
	        needsFreeTime: boolean which indicates if the client needs some free time (part of the trip needs to be not scheduled)
	        exclude: list representing the Location IDs to exclude from the trip
	        include: list representing the Location IDs to include in the trip
	        client: Client object of the custormer
	        preferenceShopping: integer from 1 to 5 which represent the preference
	        preferenceCustomer: integer from 1 to 5 which represent the preference
	        preferenceGastronomy: integer from 1 to 5 which represent the preference
	        preferenceNightLife: integer from 1 to 5 which represent the preference

	    Returns:
	        None

	        If there are no results, an empty array will be returned

	    Raises:
	        ?
	    """
		self.requirements = Requirements(startDate, numberOfDays, presenceOfKids, needsFreeTime)
		self.preferences = Preferences(preferenceShopping, preferenceCulture, preferenceGastronomy, preferenceNightLife)
		self.constraints = Constraints(exclude, include)
		self.client = client
		return 0


	def specify(self):
		''' Initializes the empty itinerary as a skeletal design, to be later filled with locations
		Args:
			self
		Returns: 
			Itinerary initialized with the correct number of days to be filled with location
		'''
		itinerary = Itinerary (self.requirements.startDate, self.requirements.days, self.client)
		return itinerary 



