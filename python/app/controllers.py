from flask import Flask
from flask import jsonify
from flask import render_template
from app import app
from app import models
from app import inference


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getClient/<q>', methods = ['GET'])
def getClient(q):
    """Fetches the clients whose name starts with the parameter q.

    Args:
        q: string which represent the prefix of the name

    Returns:
        A list of clients
        
         {"clients": [[2, "Marco"]
                    [3, "Marcello"]
        ]}

        If there are no results, an empty array will be returned

    Raises:
        ?
    """
    clientsList = models.Client.query.filter(models.Client.name.startswith(q)).all()
    response = []
    for row in clientsList:
        response.append((row['ID'], row['name']))
    return jsonify({'clients': response });


@app.route('/hello', methods = ['POST'])
def getRequest():

    if(request.form['existingClient']==0):
        client = models.Client(request.form['clientName'], request.form['clientQuiet'], request.form['clientDinamicity'])
        db.session.add(newClient)
        db.session.commit()
    else:
        client = models.Client.query.get(request.form['existingClient'])

    newReq = inference.Request()
    newReq.operationalize(request.form['startDate'], request.form['numberOfDays'], request.form['presenceOfKids'], request.form['needsFreeTime'], request.form['exclude'], request.form['include'], client, request.form['preferenceShopping'], request.form['preferenceCulture'], request.form['preferenceGastronomy'], request.form['preferenceNightLife'])
    if itinerary = newReq.specify() is None:
    	#TODO come si mandano le risposte al client tipo "400 Bad Request"?
    	return None
    return itinerary





