from flask import Flask
from flask import jsonify
from collections import namedtuple
import sqlite3
import sys

Timeslot = namedtuple("Timeslot", "morning afternoon meal evening")

class Day:
	def __init__(self):
		self.timeslot = Timeslot()

class Itinerary:
	def __init__(self, duration, client):
		if duration is 0:
			return None
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
