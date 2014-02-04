from app import app
from app import db
from app import models
from collections import namedtuple


Requirements = namedtuple("Requirements", "startDate days kids freeTime client")

class easyAround(object):
    """Class that has to propose the itinerary to the TA

    Attributes:
        None
    """
    def propose(self, requirements, preferences, sketal_design, constraints):
        """Divides all the parameters in requirements, preferences and constraints.

        Args:
            requirements: the Requirements namedtuple which represents the itinerary requirements
            preferences: the Preferences namedtuple which represents the preferences requirements
            sketal_design: A tuple composed by the itinerary Model and the days Models
            constraints: the Constraints namedtuple which represents the constraints requirements

        Returns:
            the list of the days inserted in the database (and their respective assigned locations)

        Raises:
            ?
        """
        (itinerary, days) = sketal_design

        #insert everything into the DB
        '''for exclude in constraints.exclude:
            c = models.Constraint(itinerary.ID, exclude, 'avoid')
            db.session.add(c)
        for include in constraints.include:
            c = models.Constraint(itinerary.ID, include, 'include')
            db.session.add(c)'''


        for preferenceType in preferences._fields:
            p = models.Preference(itinerary.ID, preferenceType, getattr(preferences, preferenceType))
            db.session.add(p)

        db.session.commit()

        #selectLocation
        locations, meals = itinerary.selectLocation(requirements, preferences, constraints)

        for day in sketal_design[1]:
            db.session.add(day)
            db.session.commit()

            for type in ['morning', 'afternoon', 'evening']:
                if len(locations) == 0:
                    ID = None
                else:
                    location = locations.pop()
                    ID = int(location.ID)

                timeslot = models.Timeslot(day.ID, ID, type)
                db.session.add(timeslot)

            if len(meals) == 0:
                ID = None
            else:
                location = meals.pop()
                ID = int(location.ID)
            
            timeslot = models.Timeslot(day.ID, ID, 'meal')
            db.session.add(timeslot)
            db.session.commit()

        return sketal_design[1]
            

	def critique(self, violation, itinerary):
		''' Edits the itinerary accordingly to the critique obtained from the client.
        Args:
			violation: the new set of constraints from the client
			itinerary: the old itinerary to be modified
		Returns: 
            None
		'''
		#passes control to select() and modify() to make the fix actions permanent
		if len(violation.locations) > 0:
			for locationID in violation.locations:
				itinerary.select(locationID, violation.itineraryID)
			#recovers the old preferences and requirements, and the new set of constraints obtained from the violation	
			constraints = Constraint.query.filter_by(itinerary_ID = violation.itineraryID).all() #TODO be careful during testing
			preferences = Preference.query.filter_by(itinerary_ID = violation.itineraryID).first()
			countDays = Day.query.filter_by(itinerary_ID = violation.itineraryID).count()
			days = Day.query.filter_by(itinerary_ID = violation.itineraryID).all()
			requirements = Requirements(0, countDays, itinerary.withKids, itinerary.needsFreeTime, itinerary.client_ID)
			#performs a selectLocation to chose new locations that will overwrite the violations
			locations, meals = itinerary.selectLocation(requirements, preferences, constraints)
			#assigns the new locations to the timeslots inside each day of the itinerary, updating them
			for day in days:
				for type in ['morning', 'afternoon', 'meal', 'evening']:
					if type == 'meal':
						if len(meals) == 0:
							timeslot = None
						else:
							timeslot = Timeslot.query.filter_by(day_ID = day.ID, type = type)
							location = meals.pop()
							timeslot.location_ID = int(location['ID'])
					else:
						if len(locations) == 0:
							timeslot = None
						else:
							timeslot = Timeslot.query.filter_by(day_ID = day.ID, type = type)
							location = location.pop()
							timeslot.location_ID = int(location['ID'])
					db.session.add(timeslot)
			db.session.commit()

    		


		
