import bcrypt
import mongoengine as db
from random import randrange
from datetime import datetime
from mongoengine.queryset.visitor import Q
from app.common.chk_input.user import signup_chk


class User(db.Document):
	username		= db.StringField()
	hashtext		= db.StringField()
	email			= db.EmailField()
	uniquepin		= db.StringField()
	build			= db.DateTimeField(default=datetime.utcnow)
	activeuser		= db.BooleanField(default=False)

	meta			= {
		'indexes': [
			'username',
			'email',
			'uniquepin'
		]
	}


class SetupUser():
	def __init__(self):
		pass

	def insertuser(self, username, hashtext, email):
		res = { 'status': False, 'path': 'createuser' }
		reqfields = ['id','username']
		chkinput = signup_chk(username, email)
		user = User.objects(Q(username=username) or Q(email=email)).only(*reqfields).first()
		if user:
			return res
		else:
			if len(hashtext) != 0 and chkinput == True:
				hashtext = bcrypt.hashpw(hashtext, bcrypt.gensalt(12))
				try:
					user = User(username=username, hashtext=hashtext,
								email=email, uniquepin=str(randrange(1, 9999, 4)))
					user.save()
					res = { 'status': True, 'path': 'createuser' }
					return res
				except Exception as e:
					return res
			else:
				return res

	def useractive(self, uniqpin):
		res = { 'status': False, 'path': 'activeuser' }
		reqfields = ['id','username', 'uniquepin', 'activeuser']
		if len(uniqpin) != 0:
			user = User.objects(Q(uniquepin=uniqpin) and Q(activeuser=False)).only(*reqfields).first()
			if user:
				try:
					user['activeuser'] = True
					store = user.save()
					res = { 'status': True, 'path': 'activeuser', 'user': store }
					return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res

	def checkusertoken(self, userid):
		res = { 'status': False, 'path': 'checkusertoken' }
		reqfields = ['id','username']
		if len(userid) != 0:
			try:
				user = User.objects(id=userid).only(*reqfields).first()
				if user:
					res = { 'status': False, 'path': 'checkusertoken', 'user': user }
					return res
				else:
					return res
			except Exception as e:
				return res
		else:
			return res

	def identityuser(self, identity, password):
		res = { 'status': False, 'path': 'identityuser' }
		if len(identity) and len(password) != 0:
			reqfields = ['id','username','email','hashtext']
			user = User.objects(Q(username=identity) or Q(email=identity)).only(*reqfields).first()
			if user:
				match = bcrypt.checkpw(password, user['hashtext'].encode('utf-8'))
				if match:
					res = { 'status': True, 'path': 'identityuser', 'user': user }
					return res
				else:
					return res
			else:
				return res
		else:
			return res