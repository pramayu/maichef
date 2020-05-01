import mongoengine as db
from datetime import datetime


class Blacklist(db.Document):
	token			= db.StringField()
	build			= db.DateTimeField(default=datetime.utcnow)

	meta			= {
		'indexes': [
			'token'
		]
	}


class BlacklistSetup():
	def __init__(self, token):
		self.token = token

	def inserttoken(self):
		res = { 'status': False, 'path': 'blacklist' }
		if len(self.token) != 0:
			try:
				bltoken = Blacklist(token=self.token)
				bltoken.save()
				res = { 'status': True, 'path': 'blacklist' }
				return res
			except Exception as e:
				return res
		else:
			return res


	def checktoken(self):
		res = { 'status': False, 'path': 'blacklist' }
		if len(self.token) != 0:
			bltoken = Blacklist.objects(token=self.token).first()
			if bltoken:
				res = { 'status': True, 'path': 'blacklist' }
				return res
			else:
				return res
		else:
			return res

