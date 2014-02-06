#!flask/bin/python
from app import app
from app import db
from app import Requirements
from app import Preferences
from app import Constraints
import models
from collections import namedtuple
from datetime import timedelta

class Request(object):
	"""Class that has to handle the methods operationalize and specify

    Attributes:
        requirements: the Requirements namedtuple which represents the itinerary requirements
        preferences: the Preferences namedtuple which represents the preferences requirements
        constraints: the Constraints namedtuple which represents the constraints requirements
    """
	
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

	    Raises:
	        ?
	    """
		self.requirements = Requirements(startDate, numberOfDays, presenceOfKids, needsFreeTime, client)
		self.preferences = Preferences(preferenceShopping, preferenceCulture, preferenceGastronomy, preferenceNightLife)
		self.constraints = Constraints(exclude, include)
		return 0


	def specify(self):
		"""Creates the basic structure of the itinerary (sketal_design)

	    Args:
	        None

	    Returns:
	        A tuple composed by the itinerary Model and the days Models

	    Raises:
	        ?
	    """
		# Create a new instance of itinerary in the database
		itinerary = models.Itinerary(self.requirements.kids, self.requirements.freeTime, self.requirements.client.ID)
		db.session.add(itinerary)
		db.session.commit()
		# allocate the necessary number of days for that specific itinerary, creating the skeleton
		days = []
		for i in range(0, self.requirements.days):
			day = models.Day(itinerary.ID, self.requirements.startDate + timedelta(days=i))
			days.append(day)

		return (itinerary, days)



