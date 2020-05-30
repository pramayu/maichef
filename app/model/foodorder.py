from uuid import uuid4
import mongoengine as db
from datetime import datetime
from app.model.user import Useraddress
from app.model.user import User
from app.model.foodbasket import Foodbasket
from mongoengine.queryset.visitor import Q

class Foodorder(db.Document):
	address			= db.ReferenceField(Useraddress, dbref=True)
	user 			= db.ReferenceField(User, dbref=True)
	uniqcode		= db.StringField()
	basket 			= db.ReferenceField(Foodbasket, dbref=True)
	total_mount 	= db.FloatField()
	build 			= db.DateTimeField(default=datetime.now)
	status 			= db.StringField(default="request") #request, approve, canceled

	meta 			= {
		'indexes': [
			'user',
			'uniqcode',
			'basket'
		]
	}


class SetupFoodorder():
	def __init__(self, user_id=None, basket_id=None, addr_id=None):
		self.user_id		= user_id
		self.basket_id 		= basket_id
		self.addr_id		= addr_id

	def find_basketfood(self):
		if self.user_id:
			basket = Foodbasket.objects(id=self.basket_id).first()
			return basket

	def update_basket_status(self, basket):
		if self.user_id:
			try:
				basket['status'] = not basket['status']
				basket.save()
				return True
			except Exception as e:
				return False

	def sum_mount(self, basket):
		if self.user_id:
			total_mount = 0
			temp = basket['foodchefs']
			for chef in temp:
				for item in chef['foodstuffs']:
					total_mount = total_mount + float(item['foodstuff']['price'])
			return total_mount

	def create_order(self):
		res = {'status':False, 'path': 'req_foodorder'}
		if self.user_id and self.basket_id and self.addr_id:
			user_basket = self.find_basketfood()
			if user_basket:
				try:
					total_mount = self.sum_mount(user_basket)
					if total_mount:
						foodorder = Foodorder(address=self.addr_id, user=self.user_id,
									uniqcode=uuid4().hex[:6], basket=self.basket_id,
									total_mount=float(total_mount))
						foodorder.save()
						update_basket = self.update_basket_status(user_basket)
						res = {'status':True, 'path': 'req_foodorder'}
						return res
				except Exception as e:
					return res
				else:
					return res
			else:
				return res
		else:
			return res

	def cancel_order(self, order_id):
		res = {'status':False, 'path': 'req_foodorder'}
		if self.user_id and order_id:
			pass
		else:
			pass