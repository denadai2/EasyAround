from flask import Flask
from flask import jsonify

from db.helpers import *                    #Database connection helpers
from Models.Client import Models_Client

# configuration
DATABASE = 'db/easyAround.db'
DEBUG = True


app = Flask(__name__)
app.config.from_object(__name__)

#----------------------------------------
# database helpers
#----------------------------------------

@app.before_request
def before_request():
    Flask.db = connect_db(app)
    Flask.db.row_factory = make_dicts

@app.teardown_request
def teardown_request(exception):
    Flask.db = getattr(Flask, 'db', None)
    if Flask.db is not None:
        Flask.db.close()

#----------------------------------------
# controllers
#----------------------------------------

@app.route('/')
def index():
    return "Hello, World!"

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
    clientDB = Models_Client(Flask.db)
    clientsList = clientDB.getClientList(q)
    response = []
    for row in clientsList:
        response.append((row['ID'], row['name']))
    return jsonify({'clients': response });

if __name__ == '__main__':
    app.run(debug = True)

