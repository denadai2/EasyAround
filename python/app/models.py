from app import db

class Client(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True) #cambiare nello schema
    quiet = db.Column(db.Boolean)
    dynamic = db.Column(db.Enum('1', '2', '3'))
    category = db.Column(db.Enum('young', 'adult', 'middleAged', 'elderly'))

    itineraries = db.relationship('Itinerary', backref='clients',
                                lazy='dynamic')


    def __init__(self, name, quiet, dynamic):
        self.name = name
        self.quiet = quiet
        self.dynamic = dynamic

    def __repr__(self):
        return '<Client %r>' % self.name


class Itinerary(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    withKids = db.Column(db.Boolean)
    needsFreeTime = db.Column(db.Boolean)
    client_ID = db.Column(db.Integer, db.ForeignKey('client.ID'))
    days = db.relationship('Day')


    def __init__(self, withKids, needsFreeTime, client_ID):
        self.withKids = withKids
        self.needsFreeTime = needsFreeTime
        self.client_ID = client_ID


class Contraint(db.Model):
    client_ID = db.Column(db.Integer, db.ForeignKey('client.ID'), primary_key=True)
    location_ID = db.Column(db.Integer, db.ForeignKey('location.ID'), primary_key=True)
    type = db.Column(db.Enum('avoid', 'include'))


    '''def __init__(self, name, quiet, dynamic):
        self.name = name
        self.quiet = quiet
        self.dynamic = dynamic

    def __repr__(self):
        return '<Client %r>' % self.name'''


class Preference(db.Model):
    client_ID = db.Column(db.Integer, db.ForeignKey('client.ID'), primary_key=True)
    location_ID = db.Column(db.Integer, db.ForeignKey('location.ID'), primary_key=True)
    range = db.Column(db.Enum('1', '2', '3', '4', '5'))


    '''def __init__(self, name, quiet, dynamic):
        self.name = name
        self.quiet = quiet
        self.dynamic = dynamic

    def __repr__(self):
        return '<Client %r>' % self.name'''



class Timeslot(db.Model):
    client_ID = db.Column(db.Integer, db.ForeignKey('client.ID'), primary_key=True)
    location_ID = db.Column(db.Integer, db.ForeignKey('location.ID'), primary_key=True)
    type = db.Column(db.Enum('morning', 'afternoon', 'meal', 'evening'), primary_key=True)


    def __init__(self, client_ID, location_ID, type):
        self.client_ID = client_ID
        self.location_ID = location_ID
        self.type = type


class Day(db.Model):
    itinerary_ID = db.Column(db.Integer, db.ForeignKey('itinerary.ID'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)


    def __init__(self, itinerary_ID, date):
        self.itinerary_ID = itinerary_ID
        self.date = date


class Location(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float) #cambiare nello schema
    intensive = db.Column(db.Boolean)
    rating = db.Column(db.Enum('1', '2', '3', '4', '5'))
    excludedCategory = db.Column(db.Enum('young', 'adult', 'middleAged', 'elderly'))
    forKids = db.Column(db.Boolean, default=False)

    constraints = db.relationship('Contraint', backref='locations',
                                lazy='dynamic')
    preferences = db.relationship('Preference', backref='locations',
                                lazy='dynamic')


    def __init__(self, name, quiet, dynamic):
        self.name = name
        self.quiet = quiet
        self.dynamic = dynamic

    def __repr__(self):
        return '<Client %r>' % self.name 





