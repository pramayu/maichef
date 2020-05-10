import graphene as grap
from app.model.foodstuff import SetupFoodstuff
from app.api.sekema.foodstuff.sk_foodstuff import SetupFoodstuffRes
from app.common.middleware.JSONDecoder import JSONDecoder
from app.common.middleware.authorized import requireauth


class InsertFoodStuff(grap.Mutation):

	class Arguments:
		title 			= grap.String()
		price			= grap.String()
		servtime		= grap.String()
		categories		= grap.List(grap.ID)
		userid			= grap.ID()
		chefid			= grap.ID()

	Output	= SetupFoodstuffRes

	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'insert_foodstuff' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['title']) and len(kwargs['price']) and len(kwargs['categories']) != 0:
					user_id 	= JSONDecoder(kwargs['userid'])
					chef_id		= JSONDecoder(kwargs['chefid'])
					categories 	= map(lambda x : JSONDecoder(x), kwargs['categories'])
					attribute 	= {
						'title'		: kwargs['title'],
						'price'		: kwargs['price'],
						'servtime'	: kwargs['servtime'],
						'categories': list(categories)
					}
					setup 	= SetupFoodstuff(user_id, chef_id)
					res 	= setup.insert_foodstuff(attribute)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])

class UpdateFoodStuff(grap.Mutation):

	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		foodstuffid		= grap.ID()
		title			= grap.String()
		price			= grap.String()
		servtime		= grap.String()

	Output	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'update_foodstuff' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) and len(kwargs['foodstuffid']) != 0:
				if len(kwargs['title']) and len(kwargs['price']) and len(kwargs['servtime']) != 0:
					user_id			= JSONDecoder(kwargs['userid'])
					chef_id			= JSONDecoder(kwargs['chefid'])
					foodstuff_id	= JSONDecoder(kwargs['foodstuffid'])
					attribute		= {
						'title'		: kwargs['title'],
						'price'		: kwargs['price'],
						'servtime'	: kwargs['servtime']
					}
					setup 			= SetupFoodstuff(user_id, chef_id, foodstuff_id)
					res 			= setup.update_foodstuff(attribute)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])

class UpdateFoodCategori(grap.Mutation):

	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		foodstuffid 	= grap.ID()
		categories		= grap.List(grap.String)

	Output	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'update_food_categories' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['foodstuffid']) and len(kwargs['categories']) != 0:
					user_id			= JSONDecoder(kwargs['userid'])
					chef_id			= JSONDecoder(kwargs['chefid'])
					categories		= map(lambda x: JSONDecoder(x), kwargs['categories'])
					foodstuff_id	= JSONDecoder(kwargs['foodstuffid'])
					setup 			= SetupFoodstuff(user_id, chef_id, foodstuff_id)
					res 			= setup.update_food_categories(list(categories))
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])

class PullFoodCategori(grap.Mutation):

	class Arguments:
		userid 		= grap.ID()
		chefid 		= grap.ID()
		categorid	= grap.ID()
		foodstuffid = grap.ID()

	Output	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'update_food_categories' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['categorid']) != 0:
					user_id			= JSONDecoder(kwargs['userid'])
					chef_id			= JSONDecoder(kwargs['chefid'])
					categori_id		= JSONDecoder(kwargs['categorid'])
					foodstuff_id	= JSONDecoder(kwargs['foodstuffid'])
					setup 			= SetupFoodstuff(user_id, chef_id, foodstuff_id)
					res 			= setup.pull_food_categori(categori_id)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])


class DisableFoodstuff(grap.Mutation):

	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		foodstuffid 	= grap.ID()

	Output 	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'update_foodstuff' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['foodstuffid']) != 0:
					user_id			= JSONDecoder(kwargs['userid'])
					chef_id			= JSONDecoder(kwargs['chefid'])
					foodstuff_id 	= JSONDecoder(kwargs['foodstuffid'])
					setup 			= SetupFoodstuff(user_id, chef_id, foodstuff_id)
					res 			= setup.foodstuff_disable()
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])