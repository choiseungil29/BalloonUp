#-*- coding: utf-8 -*-

from flask import request, Response
from sqlalchemy.orm.exc import NoResultFound

from index import app
from index import session

from index.models.user import User

import json

@app.route('/')
def helloWorld():
	return 'Hello World!'

@app.route('/regist', methods=['GET', 'POST'])
def registUser():
	id = request.args.get('id')
	query = session.query(User).filter_by(userId=id)

	result = {}

	try:
		query.one()
	except NoResultFound, e:
		user = User(id)
		session.add(user)
		session.commit()
		result['requestCode'] = 1
		result['requestMessage'] = u'등록되었습니다.'
		result['userId'] = user.userId
		result['highScore'] = user.score

		return json.dumps(result, ensure_ascii=False)

	user = session.query(User).filter_by(userId=id).first()

	result['requestCode'] = 2
	result['requestMessage'] = u'이미 등록되어있습니다'
	result['userId'] = user.userId
	result['highScore'] = user.score

	return json.dumps(result, ensure_ascii=False)

@app.route('/regist/score/<userId>', methods=['GET', 'POST'])
def registScore(userId):
	existUserId = existUser(userId)
	if existUserId['requestCode'] == -1:
		return json.dumps(existUserId, ensure_ascii=False)
	query = session.query(User).filter_by(userId=userId)
	result = {}
	
	user = query.first()
	if user.setScore(request.args.get('score')):
		result['requestCode'] = 1
		result['requestMessage'] = u'스코어가 갱신되었습니다.'
		result['score'] = user.score
		session.commit()
	else:
		result['requestCode'] = 2
		result['requestMessage'] = u'최고점수를 넘지 못했습니다.'

	return json.dumps(result, ensure_ascii=False)

@app.route('/get/score/<userId>', methods=['GET', 'POST'])
def getScore(userId):
	existUserId = existUser(userId)
	if existUserId['requestCode'] == -1:
		return json.dumps(existUserId, ensure_ascii=False)

	query = session.query(User).filter_by(userId=userId)
	result = {}

	user = query.first()
	result['requestCode'] = 1
	result['userId'] = user.userId
	result['score'] = user.score

	return json.dumps(result, ensure_ascii=False)

@app.route('/get/score/all', methods=['GET', 'POST'])
def getScoreAll():
	query = session.query(User).order_by(User.score.desc()).all()
	result = {}
	result['users'] = []

	for user in query:
		item = {}
		item['userId'] = user.userId
		item['score'] = user.score
		result['users'].append(item)

	result['requestCode'] = 1
	result['requestMessage'] = u'성공적으로 값을 받아왔습니다.'

	return json.dumps(result, ensure_ascii=False)

def existUser(userId):
	query = session.query(User).filter_by(userId=userId)
	result = {}

	try:
		query.one()
	except NoResultFound, e:
		result['requestCode'] = -1
		result['requestMessage'] = u'존재하지 않는 유저입니다.'
		return result
		#return json.dumps(result, ensure_ascii=False)
	result['requestCode'] = 1
	result['requestMessage'] = u'존재하는 유저입니다.'
	return result











