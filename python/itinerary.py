from flask import Flask
from flask import jsonify
import sqlite3
import sys

class Day:
	timeslot = []
	''' Note: the correspondence between timeslots is unique: 
		timeslot[1] == morning
		timeslot[2] == afternoon
		timeslot[3] == meal
		timeslot[4] == evening'''

class Itinerary:
	startDay = None
	listOfDays = []
	clientID = None
	def __init__(self, duration, client):
		if duration is 0:
			return 0
		self.clientID = client
		for i in range(0, duration):
			self.listOfDays.append(Day())
			print i
	def select(self):
		return 0
	def critique(self):
		return 0
	def modify(self):
		return 0
