import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://qjkwippgptfdlq:K70nwh86mVGdYe5R7OF_8-zGOd@ec2-50-16-238-141.compute-1.amazonaws.com:5432/d1ogcqsovf5oic"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://clogic:ok154288tmddlf@localhost/balloonup"
db = SQLAlchemy(app)

from index.models.user import User

db.create_all()
session = db.session

from index import urls

if __name__ == '__main__':
	app.run()
