from uuid import uuid4
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
	def __init__(self, user_id=None, foodstuff_id=None, basket_id=None):
		self.user_id 		= user_id
		self.foodstuff_id	= foodstuff_id
		self.basket_id 		= basket_id

	def find_basket_id(self):
		if self.user_id:
			basket = Foodbasket.objects(user=self.user_id).first()
			return basket

	def find_index_chef_id(self, chefood, chef_id):
		if self.user_id:
			indx = next((indx for (indx, i) in enumerate(chefood) if chef_id == i['chef']['id']), None)
			return indx

	def find_index_foodstuff(self, foodstuff, foodstr_id):
		if self.user_id:
			indx = next((indx for (indx, i) in enumerate(foodstuff) if foodstr_id == i['strid']), None)
			return indx

	def find_foodstuff_id(self, chef_id):
		if self.user_id and self.foodstuff_id:
			foodstuff = Foodstuff.objects(id=self.foodstuff_id).only(*['id', 'owner']).first()
			if foodstuff and chef_id == foodstuff['owner']['id']:
				return True

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
							indx = self.find_index_chef_id(chefood, chef_id)
							fstuff = chefood[indx]['foodstuffs']
							if any(self.foodstuff_id == fs['foodstuff']['id'] for fs in fstuff):
								return res
							else:
								foodstat = self.find_foodstuff_id(chef_id)
								if foodstat:
									fooditem = Fooditem(strid=uuid4().hex, foodstuff=self.foodstuff_id)
									fstuff.append(fooditem)
									basket.save()
									res = {'status': True, 'path': 'push_food'}
									return res
								else:
									return res
						else:
							foodstat = self.find_foodstuff_id(chef_id)
							if foodstat:
								foodchef = Foodchef(strid=uuid4().hex, chef=chef_id)
								fooditem = Fooditem(strid=uuid4().hex, foodstuff=self.foodstuff_id)
								foodchef['foodstuffs'].append(fooditem)
								basket['foodchefs'].append(foodchef)
								basket.save()
								res = {'status': True, 'path': 'push_food'}
								return res
							else:
								return res
					except Exception as e:
						return res
				else:
					try:
						rs_build = self.build_basket()
						if rs_build['status'] == True:
							res = self.push_foodbasket(chef_id)
							return res
						else:
							return res
					except Exception as e:
						return res
			else:
				return res
		else:
			return res

	def update_quantiti(self, chef_id, foodstr_id, quantiti):
		res = {'status': False, 'path': 'push_food'}
		if self.user_id and self.basket_id and chef_id:
			if len(foodstr_id) and len(quantiti) != 0:
				basket = self.find_basket_id()
				if basket:
					try:
						chefood = basket['foodchefs']
						if any(chef_id == chfood['chef']['id'] for chfood in chefood):
							indx = self.find_index_chef_id(chefood, chef_id)
							foodstuff = chefood[indx]['foodstuffs']
							if any(foodstr_id == food['strid'] for food in foodstuff):
								indx = self.find_index_foodstuff(foodstuff, foodstr_id)
								if foodstuff[indx]['quantities'] != int(quantiti):
									foodstuff[indx]['quantities'] = int(quantiti)
									basket.save()
									res = {'status': True, 'path': 'quantiti'}
									return res
								else:
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
		else:
			return res

	def pull_fooditem(self, chef_id, foodstr_id):
		res = {'status': False, 'path': 'pull_fooditem'}
		if self.user_id and self.basket_id and chef_id:
			if len(foodstr_id) != 0:
				basket = self.find_basket_id()
				if basket:
					try:
						chefood = basket['foodchefs']
						if any(chef_id == chfood['chef']['id'] for chfood in chefood):
							indx = self.find_index_chef_id(chefood, chef_id)
							foodstuff = chefood[indx]['foodstuffs']
							if any(foodstr_id == food['strid'] for food in foodstuff):
								indx = self.find_index_foodstuff(foodstuff, foodstr_id)
								foodstuff.pop(indx)
								basket.save()
								res = {'status': True, 'path': 'pull_fooditem'}
								return res
							else:
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
		else:
			return res