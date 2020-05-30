from uuid import uuid4
import mongoengine as db
from datetime import datetime
from app.model.foodstuff import Foodstuff
from app.model.user import User
from app.model.chef import Chef
from app.model.kitchentool import Kitchentool
from app.model.schedule import Schedulechef
from mongoengine.queryset.visitor import Q


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

class Reqschedule(db.EmbeddedDocument):
	strid 		= db.StringField()
	reqdate		= db.StringField()
	reqtime		= db.StringField()
	reqstatus	= db.StringField(default="request") #request, canceled, completed

	meta 		= {
		'indexes': [
			'strid'
		]
	}

class Foodchef(db.EmbeddedDocument):
	strid 		= db.StringField()
	chef 		= db.ReferenceField(Chef, dbref=True)
	foodstuffs 	= db.ListField(db.EmbeddedDocumentField(Fooditem))
	build	 	= db.DateTimeField(default=datetime.now)
	kitchentool	= db.ListField(db.ReferenceField(Kitchentool, dbref=True))
	ingredient	= db.BooleanField(default=False)
	reqschedule = db.EmbeddedDocumentField(Reqschedule)

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
	status 		= db.BooleanField(default=False)

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
			basket = Foodbasket.objects(Q(user=self.user_id) & Q(status=False)).first()
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

	def check_kitchen_tool(self, kitchentools, tool_id):
		if self.user_id and self.basket_id:
			if tool_id not in kitchentools:
				return True
			else:
				return False

	def find_kitchentool(self, kitchentl, kitchen_id):
		if self.user_id and self.basket_id:
			indx = next((idx for(idx, i) in enumerate(kitchentl) if i['id'] == kitchen_id), None)
			return indx

	def find_chef_schedule(self, chef_id, rq_date):
		# find with chef => datime
		if self.user_id:
			schedule = Schedulechef.objects(Q(chef=chef_id) & Q(datime=rq_date)).first()
			return schedule

	def sort_workdetail(self, workdetail):
		if self.user_id:
			works = []
			for workd in workdetail:
				if workd['status'] != 'canceled':
					works.append(workd)

			works = works.sort(key=lambda wk: datetime.strptime(wk['build'], '%Y-%m-%d'))
			return works

	def check_valid_range_schedule(self, ls_time, rq_time):
		if self.user_id:
			time_format = '%H:%M:%S'
			tdelta = datetime.strptime(rq_time, time_format) - datetime.strptime(ls_time, time_format)
			return tdelta.seconds

	def check_valid_schedule(self, schedule, rq_time):
		if self.user_id:
			if schedule['status'] == True:
				if len(schedule['workdetail']) < int(schedule['chef']['basicrule']['limit_task']):
					works = self.sort_workdetail(schedule['workdetail'])
					ls_time = schedule['workdetail'][len(works) - 1]['time']
					tmdelta = self.check_valid_range_schedule(ls_time, rq_time)
					if int(tmdelta) > int(schedule['chef']['basicrule']['range_work']):
						return True
					else:
						return False
				else:
					return False
			else:
				return False

	def req_schedule(self, rq_date, rq_time):
		if self.user_id:
			req_schedule = Reqschedule(strid=uuid4().hex, reqdate=rq_date, reqtime=rq_time)
			return req_schedule


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
						return res
				else:
					return res
			else:
				return res
		else:
			return res

	def pull_foodchef(self, chef_id):
		res = {'status': False, 'path': 'pull_foodchef'}
		if self.user_id and self.basket_id and chef_id:
			basket = self.find_basket_id()
			if basket:
				try:
					chefood = basket['foodchefs']
					if any(chef_id == chfood['chef']['id'] for chfood in chefood):
						indx = self.find_index_chef_id(chefood, chef_id)
						if len(chefood[indx]['foodstuffs']) != 0:
							return res
						else:
							chefood.pop(indx)
							basket.save()
							res = {'status': True, 'path': 'pull_foodchef'}
							return res
					else:
						return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res

	def push_kitchen_tool(self, chef_id, kitchen_id):
		res = { 'status': False, 'path': 'push_kitchen_tool' }
		if self.user_id and self.basket_id:
			if chef_id and kitchen_id:
				basket = self.find_basket_id()
				if basket:
					try:
						chefood = basket['foodchefs']
						if any(chef_id == chfood['chef']['id'] for chfood in chefood):
							indx = self.find_index_chef_id(chefood, chef_id)
							kitchentl = map(lambda x: x['id'], chefood[indx]['kitchentool'])
							for tool_id in kitchen_id:
								kt = self.check_kitchen_tool(kitchentl, tool_id)
								if kt == True:
									chefood[indx].kitchentool.append(tool_id)
							basket.save()
							res = { 'status': True, 'path': 'push_kitchen_tool' }
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

	def pull_kitchen_tool(self, chef_id, kitchen_id):
		res = { 'status': False, 'path': 'pull_kitchen_tool' }
		if self.user_id and self.basket_id:
			if chef_id and kitchen_id:
				basket = self.find_basket_id()
				if basket:
					try:
						chefood = basket['foodchefs']
						if any(chef_id == chfood['chef']['id'] for chfood in chefood):
							indx = self.find_index_chef_id(chefood, chef_id)
							kitchentl = chefood[indx]['kitchentool']
							if any(kitchen_id == i['id'] for i in kitchentl):
								indx = self.find_kitchentool(kitchentl, kitchen_id)
								kitchentl.pop(indx)
								basket.save()
								res = { 'status': True, 'path': 'pull_kitchen_tool' }
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

	def who_bought_inggr(self, chef_id):
		res = { 'status': False, 'path': 'who_bought_inggr' }
		if self.user_id and self.basket_id:
			if chef_id:
				basket = self.find_basket_id()
				if basket:
					try:
						chefood = basket['foodchefs']
						indx = self.find_index_chef_id(chefood, chef_id)
						chefood[indx]['ingredient'] = not chefood[indx]['ingredient']
						basket.save()
						res = { 'status': True, 'path': 'who_bought_inggr' }
						return res
					except Exception as e:
						return res
				else:
					return res
			else:
				return res
		else:
			return res

	def request_schedule(self, chef_id, rq_date, rq_time):
		res = {'status': False, 'path': 'req_schedule'}
		if self.user_id and self.basket_id and chef_id:
			if len(rq_date) and len(rq_time) != 0:
				basket 	= self.find_basket_id()
				if basket:
					chefood = basket['foodchefs']
					if any(chef_id == i['chef']['id'] for i in chefood):
						indx = self.find_index_chef_id(chefood, chef_id)
						schedule = self.find_chef_schedule(chef_id, rq_date)
						if schedule:
							rs = self.check_valid_schedule(schedule, rq_time)
							if rs:
								try:
									req_schedule = self.req_schedule(rq_date, rq_time)
									chefood[indx]['reqschedule'] = req_schedule
									basket.save()
									res = {'status': True, 'path': 'req_schedule'}
									return res
								except Exception as e:
									return res
							else:
								return res
						else:
							try:
								req_schedule = self.req_schedule(rq_date, rq_time)
								chefood[indx]['reqschedule'] = req_schedule
								basket.save()
								res = {'status': True, 'path': 'req_schedule'}
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

