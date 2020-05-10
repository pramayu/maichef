import mongoengine as db
from datetime import datetime
from app.model.chef import Chef
from app.model.kitchentool import Kitchentool
from app.model.categori import Categori
from app.common.chk_input.foodstuff import chk_input


class Ingredient(db.EmbeddedDocument):
	strid 			= db.StringField()
	ingredient		= db.StringField()
	number			= db.StringField()

	meta 			= {
		'indexes': [
			'strid'
		]
	}

class Foodstuff(db.Document):
	title			= db.StringField()
	slug			= db.StringField()
	price			= db.FloatField()
	status			= db.StringField(default="pending") #pending, draf, approve
	servtime		= db.StringField()
	servstatus		= db.BooleanField(default=True)
	categories		= db.ListField(db.ReferenceField(Categori, dbref=True))
	ingredients		= db.ListField(db.EmbeddedDocumentField(Ingredient))
	owner			= db.ReferenceField(Chef, dbref=True)
	kitchentool 	= db.ListField(db.ReferenceField(Kitchentool, dbref=True))
	build			= db.DateTimeField(default=datetime.utcnow)
	updated 		= db.DateTimeField()

	meta			= {
		'indexes': [
			'slug',
			'status',
			'servtime',
			'categories'
		]
	}


class SetupFoodstuff():
	def __init__(self, user_id=None, chef_id=None, foodstuff_id=None, str_id=None):
		self.user_id		= user_id
		self.chef_id		= chef_id
		self.foodstuff_id	= foodstuff_id
		self.str_id			= str_id

	def create_slug(self, title):
		slug = title.lower().replace(" ","_")
		return slug

	def find_by_slug(self, slug):
		if slug:
			fs = Foodstuff.objects(slug=slug).only(*['id']).first()
			return fs
		else:
			return False

	def find_by_id(self, req_fields):
		if self.foodstuff_id:
			foodstuff = Foodstuff.objects(id=self.foodstuff_id).only(*req_fields).first()
			return foodstuff

	def insert_foodstuff(self, attribute):
		res = { 'status': False, 'path': 'insert_foodstuff' }
		if self.user_id and self.chef_id:
			if attribute:
				is_valid = chk_input(attribute['title'], attribute['price'])
				if is_valid == True:
					slug = self.create_slug(attribute['title'])
					fs = self.find_by_slug(slug)
					if fs:
						return res
					else:
						try:
							stored = Foodstuff(title=attribute['title'],
								price=attribute['price'], owner=self.chef_id, slug=slug,
								servtime=attribute['servtime'],
								categories=attribute['categories'])
							xstored = stored.save()
							if xstored:
								res = { 'status': True, 'path': 'insert_foodstuff' }
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

	def update_foodstuff(self, attribute):
		res = { 'status': False, 'path': 'update_foodstuff' }
		if self.user_id and self.chef_id:
			if self.foodstuff_id:
				is_valid = chk_input(attribute['title'], attribute['price'])
				if is_valid:
					try:
						req_fields = ['id', 'title', 'price', 'servtime', 'slug']
						foodstuff = self.find_by_id(req_fields)
						slug = self.create_slug(attribute['title'])
						if foodstuff:
							foodstuff['slug']		= slug
							foodstuff['title']		= attribute['title']
							foodstuff['price']		= float(attribute['price'])
							foodstuff['servtime']	= attribute['servtime']
							foodstuff.save()
							res = { 'status': True, 'path': 'update_foodstuff' }
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

	def update_food_categories(self, categories):
		res = { 'status': False, 'path': 'update_food_categories' }
		if self.user_id and self.chef_id:
			if self.foodstuff_id and categories:
				req_fields = ['id', 'categories']
				foodstuff = self.find_by_id(req_fields)
				if foodstuff:
					ex_categories = map(lambda x: x['id'], foodstuff['categories'])
					for categori in categories:
						if categori not in ex_categories:
							foodstuff.categories.append(categori)
					foodstuff.save()
					res = { 'status': True, 'path': 'update_food_categories' }
					return res
					return res
				else:
					return res
			else:
				return res
		else:
			return res

	def pull_food_categori(self, categori_id):
		res = { 'status': False, 'path': 'update_food_categories' }
		if self.user_id and self.chef_id:
			if categori_id:
				try:
					req_fields = ['id', 'categories']
					foodstuff = self.find_by_id(req_fields)
					if foodstuff:
						temp = foodstuff['categories']
						if any(categori_id == x['id'] for x in temp):
							indx = next((xz for(xz, x) in enumerate(temp) if categori_id == x['id']), None)
							temp.pop(indx)
							foodstuff.save()
							res = { 'status': True, 'path': 'update_food_categories' }
							return res
						else:
							return res
					else:
						return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res

	def foodstuff_disable(self):
		res = { 'status': False, 'path': 'update_foodstuff' }
		if self.user_id and self.chef_id:
			try:
				req_fields = ['id', 'servstatus']
				foodstuff = self.find_by_id(req_fields)
				if foodstuff:
					foodstuff['servstatus'] = not foodstuff['servstatus']
					foodstuff.save()
					res = { 'status': True, 'path': 'update_foodstuff' }
					return res
				else:
					return res
			except Exception as e:
				return res
		else:
			return res


	def push_ingredient(self, ingredient):
		pass

	def pull_ingredient(self):
		pass