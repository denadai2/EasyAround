from app import app
from app import db
from app import models
from collections import namedtuple
from flask import render_template

Requirements = namedtuple("Requirements", "startDate days kids freeTime client")
Preferences = namedtuple("Preferences", "shopping culture gastronomy nightlife")
Constraints = namedtuple("Constraints", "exclude include")

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
            the itinerary and 
            the list of the days inserted in the database (and their respective assigned locations)

        Raises:
            ?
        """
        (itinerary, days) = sketal_design

        #insert constraints and preferences into the database
        for exclude in constraints.exclude:
            c = models.Constraint(itinerary.ID, models.Location.query.filter_by(name=exclude).first().ID, 'avoid')
            db.session.add(c)
        for include in constraints.include:
            c = models.Constraint(itinerary.ID, models.Location.query.filter_by(name=include).first().ID, 'include')
            db.session.add(c)
        for preferenceType in preferences._fields:
            p = models.Preference(itinerary.ID, preferenceType, getattr(preferences, preferenceType))
            db.session.add(p)

        db.session.commit()
		
		# Fetch the locations accordingly to the knowledge rules in selectLocation
        #locations: places, meals, eveningPlaces
        locations = itinerary.selectLocation(requirements, preferences, constraints)
        mapping = { 'morning': 0, 'afternoon': 0, 'meal':1, 'evening':2}
		#for each timeslot in each day, assign one of the chosen locations to fill in the itinerary
        for day in sketal_design[1]:
            db.session.add(day)
            db.session.commit()

            for type in mapping:
                if len(locations[mapping[type]]) == 0:
                    ID = None
                else:
                    location = locations[mapping[type]].pop(0)
                    ID = int(location.ID)

                timeslot = models.Timeslot(day.ID, ID, type)
                db.session.add(timeslot)


            db.session.commit()
        #return the filled skeletal design
        return sketal_design

           
    def verify(self, proposal):
        ''' submits the proposal to the client
        Args:
            proposal: the itinerary and the list of the days inserted in the database (and their respective assigned locations)
        Returns: 
            The HTML ready for the client
        '''
        return render_template('proposeItinerary.html', days=proposal[1], step=2, itinerary=proposal[0])


    def critique(self, violation, itinerary):
        ''' Edits the itinerary accordingly to the critique obtained from the client.
        Args:
            violation: the new set of constraints from the client
            itinerary: the old itinerary to be modified
        Returns: 
            The list of days of the modified itinerary
        '''
        #passes control to select() and modify() to make the fix actions permanent
        if len(violation.locations) > 0:
            for locationID in violation.locations:
                itinerary.select(locationID, violation.itineraryID)
            #recover the old preferences and requirements, and the new set of constraints obtained from the violation	
            constraintsDB = models.Constraint.query.filter_by(itinerary_ID = violation.itineraryID).all()
            excludeList = []
            includeList = []
            for constraint in constraintsDB:
                if constraint.type == 'avoid':
                    excludeList.append(constraint.location.name)
                else:
                    includeList.append(constraint.location.name)
            constraints = Constraints(excludeList, includeList)

            preferenceShopping = models.Preference.query.filter_by(itinerary_ID = violation.itineraryID, type="shopping").first()
            preferenceCulture = models.Preference.query.filter_by(itinerary_ID = violation.itineraryID, type="culture").first()
            preferenceGastronomy = models.Preference.query.filter_by(itinerary_ID = violation.itineraryID, type="gastronomy").first()
            preferenceNightLife = models.Preference.query.filter_by(itinerary_ID = violation.itineraryID, type="nightlife").first()
            preferences = Preferences(preferenceShopping.range, preferenceCulture.range, preferenceGastronomy.range, preferenceNightLife.range)

            days = models.Day.query.filter_by(itinerary_ID = violation.itineraryID).all()
            requirements = Requirements(0, len(days), itinerary.withKids, itinerary.needsFreeTime, itinerary.client)
			#performs a selectLocation to chose new locations that will overwrite the violations
			#locations: places, meals, eveningPlaces
            locations = itinerary.selectLocation(requirements, preferences, constraints)
            mapping = { 'morning': 0, 'afternoon': 0, 'meal': 1, 'evening': 2}
			#assigns the new locations to the timeslots inside each day of the itinerary, updating them
            for day in days:
                for timeslot in day.timeslots:
                    if len(locations[mapping[timeslot.type]]) == 0:
                        ID = None
                    else:
                        location = locations[mapping[timeslot.type]].pop(0)
                        ID = int(location.ID)
                    timeslot.location_ID = ID
                    db.session.add(timeslot)
            db.session.commit()

        return (itinerary, days)

    		


		
