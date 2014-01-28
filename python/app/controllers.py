from flask import Flask
from flask import jsonify
from flask import render_template
from app import app
from app import models
from app.Request import *
from app.easyAround import *

from datetime import date # temp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getClient', methods = ['POST'])
def getClient():
    """Fetches the clients whose name starts with the parameter q.

    Args:
        q: POST string which represent the prefix of the name

    Returns:
        A list of clients
        
         {"clients": [[2, "Marco"]
                    [3, "Marcello"]
        ]}

        If there are no results, an empty array will be returned

    Raises:
        ?
    """
    clientsList = models.Client.query.filter(models.Client.name.startswith(request.form['q'])).all()
    response = []
    for row in clientsList:
        response.append((row['ID'], row['name']))
    return jsonify({'clients': response });


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
	eA.critique(request, oldItinerary)
	#TODO return something to the customer
	return jsonify({'response':  'OK' });


'''@app.route('/bu', methods = ['GET'])
def getBu():

    r = Request()
    c = models.Client("Marco", True, 2, "young")
    db.session.add(c)
    db.session.commit()
    r.operationalize(date(2013, 12, 22), 2, True, True, (1,), (), c, 1, 4, 1, 1)

    sketal_design = r.specify()

    eA = easyAround()
    eA.propose(r.requirements, r.preferences, sketal_design, r.constraints)

    return itinerary'''


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
    if request.form['existingClient']==0:
        client = models.Client(request.form['clientName'], request.form['clientQuiet'], request.form['clientDinamicity'])
        db.session.add(newClient)
        db.session.commit()
    else:
        client = models.Client.query.get(request.form['existingClient'])

    day,month,year = request.form['startDate'].split('/')
    startDate = datetime.date(int(year),int(month),int(day))
    day,month,year = request.form['endDate'].split('/')
    endDate = datetime.date(int(year),int(month),int(day))
    delta = endDate - startDate

    r = Request()
    r.operationalize(date, delta.days, request.form['presenceOfKids'], request.form['needsFreeTime'], request.form['exclude'], request.form['include'], client, 
        request.form['preferenceShopping'], request.form['preferenceCulture'], request.form['preferenceGastronomy'], request.form['preferenceNightLife'])

    sketal_design = r.specify()

    eA = easyAround()
    eA.propose(r.requirements, r.preferences, sketal_design, r.constraints)


    return ''





