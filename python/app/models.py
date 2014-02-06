from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from app import db
import random

class Client(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    quiet = db.Column(db.Boolean)
    category = db.Column(db.Enum('young', 'adult', 'middleAged', 'elderly'))
    
    def __init__(self, name, quiet, category):
        self.name = name
        self.quiet = quiet
        self.category = category

    def __repr__(self):
        return '<Client %r>' % self.name


class Itinerary(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    withKids = db.Column(db.Boolean)
    needsFreeTime = db.Column(db.Boolean)
    client_ID = db.Column(db.Integer, db.ForeignKey('client.ID'))
    days = db.relationship('Day')

    client = db.relationship('Client', backref='itinerary')


    def __init__(self, withKids, needsFreeTime, client_ID):
        self.withKids = withKids
        self.needsFreeTime = needsFreeTime
        self.client_ID = client_ID


    def modify(self, constraints):
    	''' Takes the selected action and commits the modification into the database
		
        Args:
			constraints: single action that the modify commits to make it permanent
		
        Returns: -
		'''
    	db.session.add(constraints)
        db.session.commit()


    def select(self, locationID, itineraryID):
        ''' Foreach violation, selects one single action to be performed and passes the control to modify
        
        ArgS:
            locationID: the location that corresponds to the violation, the single action that needs to be selected
            itineraryID: the id of the itinerary to be modified
        
        Returns: -
        '''
        self.modify(Constraint(itineraryID, locationID, 'avoid'))


    def selectLocation(self, requirements, preferences, constraints):
        """Select all the locations based on the requirements, preferences and constraints

        Args:
            requirements: the Requirements namedtuple which represents the itinerary requirements
            preferences: the Preferences namedtuple which represents the preferences requirements
            constraints: the Constraints namedtuple which represents the constraints requirements

        Returns:
            Tuple containing the list of all the locations to be inserted in the slots, the meal locations and the 
            evening locations

            ([morning/afternoon Locations], [meal Locations], [evening Locations])

        Raises:
            -
        """
        #Calculate the number of slots needed to be fulfilled (morning, afternoon, meal, evening)
        nSlots = requirements.days * 4
        #calculate the kids locations, that needs to be inserted in the slots. 1/6 of the locations must be for kids
        nKids = 0
        if requirements.kids:
            nKids = (nSlots/6)
            nSlots = nSlots - nKids
        #if the user requires freeTime or he is young, the system will not schedule some slots
        if requirements.freeTime or  requirements.client.category == "young":
            nSlots = nSlots - requirements.days
        #list of the probabilities. Probabilities of: ['shopping', 'culture' 'gastronomy', 'nightlife']
        probabilities = self.__calculateProbabilities(preferences)

        #calculate how many locations I need to select in the categories: ['shopping', 'culture' 'gastronomy', 'nightlife']
        locationTypes = [0,0,0,0]
        pickTypes = [0,1,2,3]

        for i in range(0, nSlots):
            if locationTypes[2] == requirements.days:
                pickTypes = [0,1,3]
                probabilities = [(probabilities[0]*3)/4, (probabilities[1]*3)/4, 1-probabilities[0]-probabilities[1]]

            randomNumber = self.__random_pick(pickTypes, probabilities)
            locationTypes[randomNumber] = locationTypes[randomNumber] + 1

        # Based on the previous calculations, the number of location that have to be picked is now known
        # Proceed to build the query, that corresponds to the application of the knowledge rules in the engine.
        i = 0
        locations = []
        meals = []
        evening = []
        categoryMapping = {
            'culture': ('cultural', 'museum', 'historical'),
            'shopping': ('shopping',),
            'gastronomy': ('gastronomy',),
            'nightlife': ('entertainment', 'amusement', 'performance')
            }

        # Consider the locations to be included (constraints)
        if len(constraints.include) > 0:
            q1 = Location.query.filter((Location.excludedCategory==None) | (Location.excludedCategory!=requirements.client.category))
            q1 = q1.filter(Location.name.in_(constraints.include))
            q1 = q1.order_by(Location.rating).order_by(func.random()).limit(len(constraints.include))

            locations.extend(q1.all())

		# Choose other locations from the database, based on preferences, requirements and constraints (the 'exclude' part)
        for preferenceType in preferences._fields:
            if locationTypes[i] > 0:
                q1 = Location.query.filter(Location.category.in_(categoryMapping[preferenceType]))\
                .filter((Location.excludedCategory==None) | (Location.excludedCategory!=requirements.client.category))
                
                if not preferenceType == "gastronomy":
                    q1 = q1.filter(Location.category!='gastronomy')

                if requirements.client.quiet or requirements.client.category == "elderly":
                    q1 = q1.filter_by(intensive=False)

                if len(constraints.exclude) > 0:
                    q1 = q1.filter(~Location.name.in_(constraints.exclude))

                q1 = q1.order_by(Location.rating).order_by(func.random()).limit(locationTypes[i])
                
                if preferenceType == "nightlife":
                    evening.extend(q1.all())
                elif not preferenceType == "gastronomy":
                    locations.extend(q1.all())
                else:
                    meals.extend(q1.all())
            i = i + 1

        # Consider the presence of kids (requirements)
        if nKids > 0:
            IDsToExclude = []
            for location in locations:
                IDsToExclude.append(location.ID)

            q1 = Location.query.filter((Location.excludedCategory==None) | (Location.excludedCategory!=requirements.client.category))
            q1 = q1.filter_by(forKids=True)

            if len(constraints.exclude) > 0:
                q1 = q1.filter(~Location.ID.in_(constraints.exclude))

            # Eliminate the possibility of choosing the same location twice, given the presence of kids
            q1 = q1.filter(~Location.ID.in_(IDsToExclude))
            q1 = q1.order_by(Location.rating).order_by(func.random()).limit(nKids)
            locations.extend(q1.all())
            
        return (locations, meals, evening)


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


    def __calculateProbabilities(self, preferences):
        """It will pick one item from some_list following the probabilities list

        Args:
            preferences: Preferences data structure containing the numbers between 1 and 5 of each preference type

        Returns:
            a list containing all the probabilities for each type (['shopping', 'culture' 'gastronomy', 'nightlife'])
        
            [0.15, 0.15, 0.30, 0.40]

            which means that shopping has probability 0.15 etc...

        Raises:
            ?
        """
        probabilities = [0,0,0,0]
        sum = 0.0
        i = 0
        for preferenceType in preferences._fields:
            probabilities[i] = float(getattr(preferences, preferenceType))
            sum = sum + probabilities[i]
            i = i+1
        
        #the sum of the probabilities needs to be 1.0
        for i in range(0,4):
            probabilities[i] = float(probabilities[i]/(sum*1.0))

        return probabilities


class Constraint(db.Model):
    itinerary_ID = db.Column(db.Integer, db.ForeignKey('itinerary.ID'), primary_key=True)
    location_ID = db.Column(db.Integer, db.ForeignKey('location.ID'), primary_key=True)
    type = db.Column(db.Enum('avoid', 'include'))

    location = db.relationship('Location', backref='constraint')


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
    location_ID = db.Column(db.Integer, db.ForeignKey('location.ID'))
    type = db.Column(db.Enum('morning', 'afternoon', 'meal', 'evening'), primary_key=True)
    order = db.Column(db.Integer) #ausiliar column which helps to order the location results 

    location = db.relationship('Location', backref='timeslot')

    def __init__(self, day_ID, location_ID, type):
        self.day_ID = day_ID
        self.location_ID = location_ID
        self.type = type
        if type == 'morning':
            self.order = 1
        elif type == 'afternoon':
            self.order = 2
        elif type == 'meal':
            self.order = 3
        else:
            self.order = 4


    def __repr__(self):
        return '<Timeslot %r %r>' % (self.type, self.location)


class Day(db.Model):
    ID = db.Column(db.Integer, primary_key=True) 
    itinerary_ID = db.Column(db.Integer, db.ForeignKey('itinerary.ID'))
    date = db.Column(db.Date)

    timeslots = db.relationship('Timeslot', lazy='joined', order_by="asc(Timeslot.order)")

    def __init__(self, itinerary_ID, date):
        self.itinerary_ID = itinerary_ID
        self.date = date


class Location(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float) 
    image = db.Column(db.String(200)) 
    intensive = db.Column(db.Boolean)
    rating = db.Column(db.Enum('1', '2', '3', '4', '5'))
    excludedCategory = db.Column(db.Enum('young', 'adult', 'middleAged', 'elderly'))
    category = db.Column(db.Enum('shopping', 'cultural', 'gastronomy', 'entertainment', 'museum', 'historical', 'performance', 'outdoors', 'amusement'))
    forKids = db.Column(db.Boolean, default=False)


    def __init__(self, name, description, lat, lng, image, intensive, rating, category, excludedCategory=None, forKids=None):
        self.name = name
        self.description = description
        self.lat = lat
        self.lng = lng
        self.image = image
        self.intensive = intensive
        self.rating = rating
        self.category = category
        self.excludedCategory = excludedCategory
        self.forKids = forKids


    def __repr__(self):
        return '<Location %r>' % self.name 





