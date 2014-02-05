from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from flask import json
from flask import render_template
from app import app
from app import models
from app.Request import *
from app.easyAround import *
from collections import namedtuple
import datetime

Violation = namedtuple("Violation", "itineraryID clientID locations")

@app.route('/')
def index():
    return render_template('index.html', step=1)


@app.route('/getClients', methods = ['GET'])
def getClients():
    """Fetches the clients whose name starts with the parameter term.

    Args:
        term: GET string which represent the prefix of the name

    Returns:
        A list of clients
        
        [[2, "Marco"]
        [3, "Marcello"]]

        If there are no results, an empty array will be returned

    Raises:
        ?
    """
    term = request.args.get('term')
    # Fetch the clients from the database according to the starting term
    clientsList = models.Client.query.filter(models.Client.name.startswith(term)).all()
    response = []
    for row in clientsList:
        dict = {'value': row.ID, 'label': row.name}
        response.append(dict)
    return Response(json.dumps(response),  mimetype='application/json')


@app.route('/getLocations', methods = ['GET'])
def getLocations():
    """Fetches the Locations whose name starts with the parameter term.

    Args:
        term: GET string which represent the prefix of the name

    Returns:
        A list of locations
        
         [[2, "Villa Borghese"]
            [3, "Villano ristorante"]]

        If there are no results, an empty array will be returned
    """
    term = request.args.get('q')
    # Fetch the locations from the database according to the starting term
    locationsList = models.Location.query.filter(models.Location.name.startswith(term)).all()
    response = []
    for row in locationsList:
        response.append((row.ID, row.name))
    return jsonify(response);


@app.route('/excludeLocations', methods = ['POST'])
def excludeLocations():
	'''Exclude a list of locations from an itinerary
		Args:
			itineraryID: POST variable which represent the ID of the considered itinerary
			clientID: POST variable which represent the ID of the client
			locations: POST variable which represent the list of locations ID to be excluded

		Returns:
		   The new itinerary with the requested modifications
		Raises:
		? '''
	# Recover the itinerary to be modified
	oldItinerary = Itinerary.query.filter_by(ID = request.form['itineraryID']).first()
	eA = easyAround()
	# Collect the violation from the customer's input
	locations = request.form.get('locations').replace('["', "").replace('"]', "").split('","')
	violation = Violation(request.form['itineraryID'], request.form['clientID'], locations)
	# Proceed in applying the modifications and submit again the itinerary to the customer
	days = eA.critique(violation, oldItinerary)
	verify = eA.verify(days)
	return verify


@app.route('/proposeItinerary', methods = ['POST'])
def getItinerary():
    """Calculate the intinerary and present it to the TA

    Args:
        startDate: start date of the trip
        endDate: end date of the trip
		presenceOfKids: boolean that indicates the presence of kids
		needsFreeTime: boolean that indicates the need for free time
		exclude: list of locations to be excluded
		include: list of locations to be included
		existingClient: identifier of the customer (if is a new customer, this equals zero)
		clientName: name of the client
		clientQuiet: the preference of the client towards quiet environment
		preferenceShopping: preference towards shopping activities, in a range from 1 to 5
		preferenceCulture: preference towards cultural activities, in a range from 1 to 5
		preferenceGastronomy: preference towards gastronomy, in a range from 1 to 5
		preferenceNightLife: preference towards nightlife activities, in a range from 1 to 5

    Returns:
        The HTML page with the calculated itinerary
    """
    print request.form
    #if the request comes from a new customer, insert them into the database
    if request.form['existingClient'] == '0':
        clientQuiet = request.form.get('clientQuiet', False)
        if clientQuiet == 'yes':
            clientQuiet = True
        client = models.Client(request.form['clientName'], clientQuiet, 'elderly')
        db.session.add(client)
        db.session.commit()
    else:
        client = models.Client.query.get(request.form['existingClient'])
    
    # Handle the data from the request form, parsing the strings to obtain manageable data types.
    month,day,year = request.form['startDate'].split('/')
    startDate = datetime.date(int(year), int(month), int(day))
    month,day,year = request.form['endDate'].split('/')
    endDate = datetime.date(int(year), int(month), int(day))
    delta = endDate - startDate
    needsFreeTime = True if request.form.get('needsFreeTime', False) == "yes" else False 
    presenceOfKids = True if request.form.get('presenceOfKids', False) == "yes" else False 
    excludeList = request.form.get('exclude').replace('["', "").replace('"]', "").split('","')
    includeList = request.form.get('include').replace('["', "").replace('"]', "").split('","')
    if excludeList[0] == "[]":
        excludeList = []
    if includeList[0] == "[]":
        includeList = []
        
    # Divide coherently the initial request calling operationalize
    r = Request()
    r.operationalize(startDate, delta.days, presenceOfKids, needsFreeTime, excludeList, includeList, client, 
        request.form['preferenceShopping'], request.form['preferenceCulture'], request.form['preferenceGastronomy'], request.form['preferenceNightLife'])
    # Create the initial skeletal design
    sketal_design = r.specify()
	# Compose the itinerary according to the knowledge rules
    eA = easyAround()
    days = eA.propose(r.requirements, r.preferences, sketal_design, r.constraints)
    # Hand out the first version of the itinerary to the client, to allow modifications
    verify = eA.verify(days)

    return verify





