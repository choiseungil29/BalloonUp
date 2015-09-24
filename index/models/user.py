
import os
import binascii

from sqlalchemy.dialects import postgresql

from index import db

class User(db.Model):
	__tablename__ = 'user'

	userId = db.Column(db.String(), primary_key=True)
	score = db.Column(db.Integer())

	def __init__(self, userId):
		self.userId = userId
		self.score = 0

	def __repr__(self):
		return '<id {}>'.format(self.userId)

	def setScore(self, score):
		if self.score < int(score):
			self.score = int(score)
			return True
		return False

