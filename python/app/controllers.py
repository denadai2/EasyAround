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

    Raises:
        ?
    """
    term = request.args.get('q')
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
	oldItinerary = Itinerary.query.filter_by(ID = request.form['itineraryID']).first()
	eA = easyAround()
	locations = request.form.get('locations').replace('["', "").replace('"]', "").split('","')
	violation = Violation(request.form['itineraryID'], request.form['clientID'], locations)
	days = eA.critique(violation, oldItinerary)
	return render_template('proposeItinerary.html', days=days, step=2)


@app.route('/proposeItinerary', methods = ['POST'])
def getItinerary():
    """Calculate the intinerary and present it to the TA

    Args:
        mio dio nn ho voglia ora

    Returns:
        The HTML page with the calculated itinerary

    Raises:
        ?
    """
    print request.form
    if request.form['existingClient'] == '0':
        clientQuiet = request.form.get('clientQuiet', False)
        if clientQuiet == 'yes':
            clientQuiet = True
        client = models.Client(request.form['clientName'], clientQuiet, 'elderly')
        db.session.add(client)
        db.session.commit()
    else:
        client = models.Client.query.get(request.form['existingClient'])
    
    month,day,year = request.form['startDate'].split('/')
    startDate = datetime.date(int(year), int(month), int(day))
    month,day,year = request.form['endDate'].split('/')
    endDate = datetime.date(int(year), int(month), int(day))
    delta = endDate - startDate

    #Form handler
    needsFreeTime = True if request.form.get('needsFreeTime', False) == "yes" else False 
    presenceOfKids = True if request.form.get('presenceOfKids', False) == "yes" else False 
    excludeList = request.form.get('exclude').replace('["', "").replace('"]', "").split('","')
    includeList = request.form.get('include').replace('["', "").replace('"]', "").split('","')
    if excludeList[0] == "[]":
        excludeList = []
    if includeList[0] == "[]":
        includeList = []
    
    r = Request()
    r.operationalize(startDate, delta.days, presenceOfKids, needsFreeTime, excludeList, includeList, client, 
        request.form['preferenceShopping'], request.form['preferenceCulture'], request.form['preferenceGastronomy'], request.form['preferenceNightLife'])
    sketal_design = r.specify()

    eA = easyAround()
    days = eA.propose(r.requirements, r.preferences, sketal_design, r.constraints)


    return render_template('proposeItinerary.html', days=days, step=2)





