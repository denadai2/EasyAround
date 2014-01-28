from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app import db
import random

import logging

logging.basicConfig(filename='db.log')
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class Client(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200)) #, unique=True
    quiet = db.Column(db.Boolean)
    dynamic = db.Column(db.Enum('1', '2', '3'))
    category = db.Column(db.Enum('young', 'adult', 'middleAged', 'elderly'))

    itineraries = db.relationship('Itinerary', backref='clients', lazy='dynamic')


    def __init__(self, name, quiet, dynamic, category):
        self.name = name
        self.quiet = quiet
        self.dynamic = dynamic
        self.category = category

    def __repr__(self):
        return '<Client %r>' % self.name


class Itinerary(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    withKids = db.Column(db.Boolean)
    needsFreeTime = db.Column(db.Boolean)
    client_ID = db.Column(db.Integer, db.ForeignKey('client.ID'))
    days = db.relationship('Day')

    constraints = db.relationship('Constraint', backref='locations',
                                lazy='dynamic')
    preferences = db.relationship('Preference', backref='locations',
                                lazy='dynamic')


    def __init__(self, withKids, needsFreeTime, client_ID):
        self.withKids = withKids
        self.needsFreeTime = needsFreeTime
        self.client_ID = client_ID
				
	def	select(self, locationID, itineraryID):
		''' Foreach violation, selects one single action to be performed and passes the control to modify
		ArgS:
			locationID: the location that corresponds to the violation, the single action that needs to be selected
			itineraryID: the id of the itinerary to be modified
		Returns: -
		'''
		c = models.Constraint(itineraryID, locationID, 'avoid')
        self.modify(c)
    
    def modify(constraints):
    	''' Takes the selected action and commits the modification into the database
		ArgS:
			constraints: single action that the modify commits to make it permanent
		Returns: -
		'''
    	session.db.add(constraints)
        session.db.commit()

    def selectLocation(self, requirements, preferences, constraints):
        """Select all the locations based on the requirements, preferences and constraints

        Args:
            requirements: the Requirements namedtuple which represents the itinerary requirements
            preferences: the Preferences namedtuple which represents the preferences requirements
            constraints: the Constraints namedtuple which represents the constraints requirements

        Returns:
            Tuple containing the list of all the locations to be inserted in the slots and the meal locations

        Raises:
            ?
        """
        #Calculate the number of slots needed to be fulfilled
        nSlots = requirements.days * 3
        #calculate the kids locations, that needs to be inserted in the slots. 1/6 of the locations must be for kids
        nKids = 0
        if requirements.kids:
            nKids = (nSlots/6)
            nSlots = nSlots - nKids
        #list of the probabilities. Probabilities of: ['shopping', 'culture' 'gastronomy', 'nightlife']
        probabilities = [0,0,0,0]
        sum = 0
        i = 0
        for preferenceType in preferences._fields:
            probabilities[i] = getattr(preferences, preferenceType)
            sum = sum + probabilities[i]
            i = i+1
        
        for i in range(0,4):
            probabilities[i] = float(probabilities[i]/(sum*1.0))

        #calculates how many locations I need to select in the categories: ['shopping', 'culture' 'gastronomy', 'nightlife']
        locationTypes = [0,0,0,0]

        for i in range(0, nSlots):
            randomNumber = self.__random_pick([0,1,2,3], probabilities)
            locationTypes[randomNumber] = locationTypes[randomNumber] + 1


        #now we know how many locations types we need to pick from the DB
        i = 0
        locations = []
        meals = []
        for preferenceType in preferences._fields:
            if locationTypes[i] > 0:
                q1 = Location.query.filter_by(category=preferenceType).filter(Location.excludedCategory!=requirements.client.category)

                if not preferenceType == "gastronomy":
                    q1 = q1.filter(Location.category!='gastronomy')

                if requirements.client.quiet:
                    q1 = q1.filter_by(intensive=False)

                if len(constraints.exclude) > 0:
                    q1 = q1.filter(~Location.ID.in_(constraints.exclude))

                q1 = q1.limit(locationTypes[i])

                if not preferenceType == "gastronomy":
                    locations.append(q1.all())
                else:
                    meals.append(q1.all())
            i = i + 1


        if nKids > 0:
            q1 = Location.query.filter_by(category=preferenceType).filter(Location.excludedCategory!=requirements.client.category)
            q1 = q1.filter_by(forKids=True)

            if len(constraints.exclude) > 0:
                    q1 = q1.filter(~Location.ID.in_(constraints.exclude))

            q1 = q1.limit(nKids)

            locations.append(q1.all())

      
        #Now I have all the results, I should calculate the distances, but I will not XD



        return (locations, meals)


    def __random_pick(self, some_list, probabilities):
        """It will pick one item from some_list following the probabilities list

        Args:
            some_list: list of items
            probabilities: list of probabilities associated to the items

        Returns:
            the randomly picked item

        Raises:
            ?
        """
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(some_list, probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability: 
                break
        return item


class Constraint(db.Model):
    itinerary_ID = db.Column(db.Integer, db.ForeignKey('itinerary.ID'), primary_key=True)
    location_ID = db.Column(db.Integer, db.ForeignKey('location.ID'), primary_key=True)
    type = db.Column(db.Enum('avoid', 'include'))


    def __init__(self, itinerary_ID, location_ID, type):
        self.itinerary_ID = itinerary_ID
        self.location_ID = location_ID
        self.type = type


class Preference(db.Model):
    itinerary_ID = db.Column(db.Integer, db.ForeignKey('itinerary.ID'), primary_key=True)
    type = db.Column(db.Enum('shopping', 'culture', 'gastronomy', 'nightlife'), primary_key=True)
    range = db.Column(db.Enum('1', '2', '3', '4', '5'))


    def __init__(self, itinerary_ID, type, range):
        self.itinerary_ID = itinerary_ID
        self.type = type
        self.range = range



class Timeslot(db.Model):
    day_ID = db.Column(db.Integer, db.ForeignKey('day.ID'), primary_key=True)
    location_ID = db.Column(db.Integer, db.ForeignKey('location.ID'), primary_key=True)
    type = db.Column(db.Enum('morning', 'afternoon', 'meal', 'evening'), primary_key=True)


    def __init__(self, client_ID, location_ID, type):
        self.client_ID = client_ID
        self.location_ID = location_ID
        self.type = type


class Day(db.Model):
    ID = db.Column(db.Integer, primary_key=True) 
    itinerary_ID = db.Column(db.Integer, db.ForeignKey('itinerary.ID'))
    date = db.Column(db.Date)

    timeslots = db.relationship('Timeslot', lazy='dynamic')

    def __init__(self, itinerary_ID, date):
        self.itinerary_ID = itinerary_ID
        self.date = date


class Location(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float) 
    intensive = db.Column(db.Boolean)
    rating = db.Column(db.Enum('1', '2', '3', '4', '5'))
    excludedCategory = db.Column(db.Enum('young', 'adult', 'middleAged', 'elderly'))
    category = db.Column(db.Enum('shopping', 'cultural', 'gastronomic', 'entertainment', 'museum', 'historical', 'performance', 'outdoors', 'amusement'))
    forKids = db.Column(db.Boolean, default=False)


    def __init__(self, name, description, lat, lng, intensive, rating, type, excludedCategory=None, forKids=None):
        self.name = name
        self.description = description
        self.lat = lat
        self.lng = lng
        self.intensive = intensive
        self.rating = rating
        self.type = type
        self.excludedCategory = excludedCategory
        self.forKids = forKids

    def __repr__(self):
        return '<Location %r>' % self.name 





