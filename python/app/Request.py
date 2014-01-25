#!flask/bin/python
from app import app
from app import db
import models
from collections import namedtuple
from datetime import timedelta

#---------------
# Classes and data structures
#---------------

Requirements = namedtuple("Requirements", "startDate days kids freeTime client")
Preferences = namedtuple("Preferences", "shopping culture gastronomy nightlife")
Constraints = namedtuple("Constraints", "exclude include")


# Note: changed class name from "Requirements" to "Request" otherwise it will get messed up
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
		itinerary = models.Itinerary(self.requirements.kids, self.requirements.freeTime, self.requirements.client.ID)
		db.session.add(itinerary)
		db.session.commit()

		days = []
		for i in range(0, self.requirements.days):
			day = models.Day(itinerary.ID, self.requirements.startDate + timedelta(days=i))
			days.append(day)

		return (itinerary, days)



