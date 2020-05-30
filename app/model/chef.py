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
	year_honour		= db.StringField()
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
			'strid',
			'status',
			'publicid'
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
	limit_task		= db.StringField()
	range_work 		= db.StringField() #convert to seconds
	rules			= db.ListField(db.StringField())

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

	def find_chef_id(self, req_fields):
		try:
			chef = Chef.objects(id=self.chef_id).only(*req_fields).first()
			return chef
		except Exception as e:
			return []
		
	def push_experience(self, occupation, length_of_work, work_palce):
		res = { 'status': False, 'path':'experience' }
		if self.user_id and self.chef_id:
			if len(length_of_work) and len(work_palce) != 0:
				if occupation:
					req_fields = ['id','experience']
					chef = self.find_chef_id(req_fields)
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
					chef = chef = self.find_chef_id(req_fields)
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
			chef = chef = self.find_chef_id(req_fields)
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

	def push_honour(self, instit, year_honour, in_the_field):
		res = { 'status': False, 'path':'honour' }
		if self.user_id and self.chef_id:
			if len(instit) and len(year_honour) and len(in_the_field) != 0:
				try:
					req_fields = ['id','honour']
					chef = self.find_chef_id(req_fields)
					if chef:
						honour = Honour(institution=instit,
										strid=uuid4().hex,
										year_honour=year_honour,
										in_the_field=in_the_field)
						chef.honour.append(honour)
						chef.save()
						res = { 'status': True, 'path':'honour' }
						return res
					else:
						return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res

	def pull_honour(self):
		res = { 'status': False, 'path':'honour' }
		if self.user_id and self.chef_id:
			if len(self.str_id) != 0:
				try:
					req_fields = ['id', 'honour']
					chef = self.find_chef_id(req_fields)
					temp = chef['honour']
					if any(self.str_id == hnr['strid'] for hnr in temp):
						Chef.objects(id=self.chef_id).update_one(pull__honour__strid=self.str_id)
						res = { 'status': True, 'path':'honour' }
						return res
					else:
						return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res

	def push_service_area(self, service_area):
		res = { 'status': False, 'path':'servicearea' }
		if self.user_id and self.chef_id:
			if len(service_area) != 0:
				try:
					req_fields = ['id', 'servicearea']
					chef = self.find_chef_id(req_fields)
					if chef:
						servicearea = ServiceArea(strid=uuid4().hex, areas=service_area)
						chef.servicearea.append(servicearea)
						chef.save()
						res = { 'status': True, 'path':'servicearea' }
						return res
					else:
						return res
				except Exception as e:
					print(e)
					return res
			else:
				return res
		else:
			return res

	def pull_service_area(self):
		res = { 'status': False, 'path':'servicearea' }
		if self.user_id and self.chef_id:
			if len(self.str_id) != 0:
				req_fields = ['id', 'servicearea']
				chef = self.find_chef_id(req_fields)
				if chef:
					try:
						Chef.objects(id=self.chef_id).update_one(pull__servicearea__strid=self.str_id)
						res = { 'status': True, 'path':'servicearea' }
						return res
					except Exception as e:
						return res
				else:
					return res
			else:
				return res
		else:
			return res

	def store_basic_rule(self, limit_task, range_work, rules):
		res = { 'status': False, 'path':'rule' }
		if self.user_id and self.chef_id:
			if len(limit_task) and len(rules) != 0:
				req_fields = ['id']
				chef = self.find_chef_id(req_fields)
				work = int(range_work) * 3600
				if chef:
					try:
						basic_rule = BasicRule(strid=uuid4().hex,range_work=str(work),limit_task=limit_task,rules=rules)
						chef.basicrule = basic_rule
						chef.save()
						res = { 'status': True, 'path':'rule' }
						return res
					except Exception as e:
						return res
				else:
					return res
			else:
				return res
		else:
			return res

	def update_basic_rule(self, limit_task, range_work, rules):
		res = { 'status': False, 'path':'rule' }
		if self.user_id and self.chef_id:
			if len(self.str_id) and len(limit_task) and len(rules) != 0:
				req_fields = ['id', 'basicrule']
				chef = self.find_chef_id(req_fields)
				if chef:
					try:
						temp = chef['basicrule']
						if temp['strid'] == self.str_id:
							temp['limit_task'] = limit_task
							temp['range_work'] = range_work
							temp['rules'] = rules
							chef.save()
							res = { 'status': True, 'path':'rule' }
							return res
						else:
							return res
					except Exception as e:
						return res
				else:
					return res
			else:
				return res
		else:
			return res

	def indx_image_true(self, temp):
		indx = next((index for (index, img) in enumerate(temp) if img['status'] == True), None)
		return indx

	def upload_chef_img(self, url, tipe, publicid):
		res = { 'status': False, 'path':'upload' }
		if self.user_id and self.chef_id:
			if len(url) and len(tipe) and len(publicid) != 0:
				req_fields = ['id', 'picture']
				chef = self.find_chef_id(req_fields)
				if chef:
					try:
						temp = chef['picture']
						if len(temp) != 0:
							indx = self.indx_image_true(temp)
							temp[indx]['status'] = False
						que_img = Picture(strid=uuid4().hex, url=url, tipe=tipe, publicid=publicid)
						chef.picture.append(que_img)
						chef.save()
						res = { 'status': True, 'path':'upload' }
						return res
					except Exception as e:
						return res
				else:
					return res
			else:
				return res
		else:
			return res

	def reuse_chef_img(self):
		res = { 'status': False, 'path':'upload' }
		if self.user_id and self.chef_id:
			if len(self.str_id):
				req_fields = ['id','picture']
				chef = self.find_chef_id(req_fields)
				temp = chef['picture']
				if any(self.str_id == img['strid'] for img in temp):
					try:
						indx1 = self.indx_image_true(temp)
						indx2 = next((index for (index, img) in enumerate(temp) if self.str_id == img['strid']), None)
						temp[indx1]['status'] = not temp[indx1]['status']
						temp[indx2]['status'] = not temp[indx2]['status']
						chef.save()
						res = { 'status': True, 'path':'upload' }
						return res
					except Exception as e:
						return res
				else:
					return res
			else:
				return res
		else:
			return res