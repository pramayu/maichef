import mongoengine as db
from datetime import datetime
from app.model.user import User
from app.model.chef import Chef
from app.model.foodstuff import Foodstuff


class Fooditem(db.EmbeddedDocument):
	strid 		= db.StringField()
	foodstuff 	= db.ReferenceField(Foodstuff, dbref=True)
	quantities	= db.IntField(default=1)

	meta		= {
		'indexes': [
			'strid',
			'foodstuff'
		]
	}

class Foodchef(db.EmbeddedDocument):
	strid 		= db.StringField()
	chef 		= db.ReferenceField(Chef, dbref=True)
	foodstuffs 	= db.ListField(db.EmbeddedDocumentField(Fooditem))
	build	 	= db.DateTimeField(default=datetime.now)

	meta 		= {
		'indexes': [
			'strid',
			'chef'
		]
	}
	

class Foodbasket(db.Document):
	user 		= db.ReferenceField(User, dbref=True)
	foodchefs 	= db.ListField(db.EmbeddedDocumentField(Foodchef))
	updated		= db.DateTimeField(default=datetime.now)

	meta 		= {
		'indexes': [
			'user'
		]
	}



class SetupFoodBasket():
	def __init__(self, user_id=None, foodstuff_id=None):
		self.user_id 		= user_id
		self.foodstuff_id	= foodstuff_id

	def find_basket_id(self):
		if self.user_id:
			basket = Foodbasket.objects(user=self.user_id).first()
			return basket

	def find_index_chef_id(self, chefood, chef_id):
		if self.user_id:
			indx = next((indx for (indx, i) in enumerate(chefood) if chef_id == i['chef']['id']), None)
			return indx

	def build_basket(self):
		res = {'status': False, 'path': 'build_basket'}
		if self.user_id:
			basket = self.find_basket_id()
			if basket:
				return res
			else:
				try:
					build = Foodbasket(user=self.user_id)
					build.save()
					res = {'status': True, 'path': 'build_basket'}
					return res
				except Exception as e:
					raise e
					return res
		else:
			return res

	def push_foodbasket(self, chef_id):
		res = {'status': False, 'path': 'push_food'}
		if self.user_id and self.foodstuff_id:
			if chef_id:
				basket = self.find_basket_id()
				if basket:
					try:
						chefood = basket['foodchefs']
						if any(chef_id == chfood['chef']['id'] for chfood in chefood):
							#update user food by chef
							indx = self.find_index_chef_id(chefood, chef_id)
						else:
							#push new chef
							pass
					except Exception as e:
						raise e
						return res
				else:
					return res
			else:
				return res
		else:
			return res