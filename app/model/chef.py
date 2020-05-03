from uuid import uuid4
import mongoengine as db
from datetime import datetime
from app.model.user import User
from app.model.occupation import Occupation



class Experience(db.EmbeddedDocument):
	strid 			= db.StringField()
	occupation		= db.ReferenceField(Occupation, dbref=True)
	length_of_work	= db.ListField(db.DateTimeField())
	work_palce		= db.StringField()

	meta			= {
		'indexes': [
			'strid'
		]
	}

class Honour(db.EmbeddedDocument):
	strid 			= db.StringField()
	institution		= db.StringField()
	year_honour		= db.DateTimeField()
	in_the_field	= db.StringField()

	meta			= {
		'indexes': [
			'strid'
		]
	}

class Picture(db.EmbeddedDocument):
	strid 			= db.StringField()
	url 			= db.StringField()
	publicid		= db.StringField()
	tipe			= db.StringField()
	status			= db.BooleanField(default=True)

	meta			= {
		'indexes': [
			'strid'
		]
	}

class ServiceArea(db.EmbeddedDocument):
	strid 			= db.StringField()
	areas			= db.StringField()

	meta			= {
		'indexes': [
			'strid',
			'areas'
		]
	}

class BasicRule(db.EmbeddedDocument):
	strid 			= db.StringField()
	limitask		= db.StringField()
	another			= db.ListField(db.StringField())

	meta 			= {
		'indexes': [
			'strid'
		]
	}

class Chef(db.Document):
	chefname		= db.StringField()
	build			= db.DateTimeField(default=datetime.utcnow)
	user			= db.ReferenceField(User, dbref=True)
	status			= db.StringField(default="draf") #draf, pending, approve
	experience 		= db.ListField(db.EmbeddedDocumentField(Experience))
	picture 		= db.ListField(db.EmbeddedDocumentField(Picture))
	honour			= db.ListField(db.EmbeddedDocumentField(Honour))
	servicearea 	= db.ListField(db.EmbeddedDocumentField(ServiceArea))
	basicrule 		= db.EmbeddedDocumentField(BasicRule)

	meta 			= {
		'indexes': [
			'user',
			'status',
			'build'
		]
	}



class SetupChef():

	def __init__(self, user_id=None, chef_id=None, str_id=None):
		self.user_id 	= user_id
		self.chef_id 	= chef_id
		self.str_id		= str_id

	def be_chef(self):
		res = { 'status': False, 'path':'chef' }
		if self.user_id:
			try:
				chef = Chef(user=self.user_id)
				store = chef.save()
				res = { 'status': True, 'path':'chef', 'chef': store }
				return res
			except Exception as e:
				return res
		else:
			return res

	def chk_chef(self):
		res = { 'status': False, 'path':'chef' }
		if self.user_id:
			try:
				chef = Chef.objects(user=self.user_id).only(*['id']).first()
				if chef:
					res = { 'status': True, 'path':'chef', 'chef': chef }
					return res
				else:
					return res
			except Exception as e:
				return res
		else:
			return res

	def push_experience(self, occupation, length_of_work, work_palce):
		res = { 'status': False, 'path':'experience' }
		if self.user_id and self.chef_id:
			if len(length_of_work) and len(work_palce) != 0:
				if occupation:
					req_fields = ['id','experience']
					chef = Chef.objects(id=self.chef_id).only(*req_fields).first()
					if chef:
						try:
							expr = Experience(strid=uuid4().hex,
											occupation = occupation,
											length_of_work= length_of_work,
											work_palce=work_palce)
							chef.experience.append(expr)
							chef.save()
							res = { 'status': True, 'path':'experience' }
							return res
						except Exception as e:
							print(e)
							return res
					else:
						return res
				else:
					return res
			else:
				return res
		else:
			return res

	def edit_experience(self, occupation, length_of_work, work_palce):
		res = { 'status': False, 'path':'experience' }
		if self.user_id and self.chef_id and self.str_id:
			if len(length_of_work) and len(work_palce) != 0:
				if occupation:
					req_fields = ['id','experience']
					chef = Chef.objects(id=self.chef_id).only(*req_fields).first()
					if any(self.str_id == expr['strid'] for expr in chef['experience']):
						try:
							temp = chef['experience']
							indx = next((index for (index, expr) in enumerate(temp) if self.str_id == expr['strid']), None)
							temp[indx]['occupation'] = occupation
							temp[indx]['length_of_work'] = length_of_work
							temp[indx]['work_palce'] = work_palce
							chef.save()
							res = { 'status': True, 'path':'experience' }
							return res
						except Exception as e:
							return res
					else:
						return res
				else:
					return res
			else:
				return res
		else:
			return res

	def pull_experience(self):
		res = { 'status': False, 'path':'experience' }
		if self.user_id and self.chef_id and self.str_id:
			req_fields = ['id', 'experience']
			chef = Chef.objects(id=self.chef_id).only(*req_fields).first()
			temp = chef['experience']
			if any(self.str_id == expr['strid'] for expr in temp):
				try:
					Chef.objects(id=self.chef_id).update_one(pull__experience__strid=self.str_id)
					res = { 'status': True, 'path':'experience' }
					return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res
