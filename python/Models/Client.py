from db.helpers import *

class Models_Client():

    def __init__(self, db):
        self.db = db

    def create(self, name, dynamic, quiet):
    	clientsList = db.execute('INSERT INTO client (name, dynamic, quiet)');
    	return db.commit()

    def getClientList(self, prefix):
    	prefix = prefix+"%"
    	clientsList = query_db('select name, ID from client WHERE name LIKE ? ORDER BY name', [prefix]);
    	return clientsList
    