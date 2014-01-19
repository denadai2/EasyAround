from flask import Flask
from flask import jsonify
import sqlite3
from contextlib import closing
from itinerary import *
import json
import sys

class Requirements:
	requirements = []
	preferences = []
	constraints = []
	''' Class that has to handle the methods operationalize and specify.'''
	def operationalize(self):
		return 0
	def specify(self):
		'''Assuming an array (dictionary is a possibility) of requirements as follows
		numberOfDays: int
		presenceOfKids: boolean
		needsFreeTime: boolean
		existingClient: int (ID o 0)
		clientName: string
		clientDinamicity: int
		clientQuiet: boolean
		'''
		itinerary = Itinerary ((self.constraints['numberOfDays'], self.constraints['existingClient']))
		return itinerary 
		
def main(argv=None):
	req = Requirements()
	print req.specify()


if __name__ == "__main__":
    sys.exit(main())

