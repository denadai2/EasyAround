from flask import Flask
from flask import jsonify
import sqlite3
from contextlib import closing

# configuration
DATABASE = 'db/easyAround.db'
DEBUG = True



app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def make_dicts(cur, row):
    return dict((cur.description[idx][0], value) for idx, value in enumerate(row))

def query_db(query, args=(), one=False):
    cur = Flask.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    Flask.db = connect_db()
    Flask.db.row_factory = make_dicts

@app.teardown_request
def teardown_request(exception):
    db = getattr(Flask, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/getClient/<q>', methods = ['GET'])
def getClient(q):
    """Fetches the clients whose name starts with the parameter q.

    Args:
        q: string which represent the prefix of the name

    Returns:
        A list of clients

        {'Serak': ('Rigel VII', 'Preparer'),
         'Zim': ('Irk', 'Invader'),
         'Lrrr': ('Omicron Persei 8', 'Emperor')}

         {"clients": [[2, "Marco"]
                    [3, "Marcello"]
        ]}

        If there are no results, an empty array will be returned

    Raises:
        ?
    """
    pass
    q = q+"%"
    clientsList = query_db('select name, ID from client WHERE name LIKE ? ORDER BY name', [q]);
    response = []
    for row in clientsList:
        response.append((row['ID'], row['name']))
    return jsonify({'clients': response });

if __name__ == '__main__':
    app.run(debug = True)

