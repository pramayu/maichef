import graphene as grap
from app.model.foodbasket import SetupFoodBasket
from app.api.sekema.buildbasket.sk_buildbasket import SetupFoodBasketRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder



class PushFoodBasket(grap.Mutation):

	class Arguments:
		userid			= grap.ID()
		chefid			= grap.ID()
		foodstuffid		= grap.ID()

	Output 	= SetupFoodBasketRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'push_food'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['foodstuffid']) != 0:
					user_id 		= JSONDecoder(kwargs['userid'])
					foodstuff_id	= JSONDecoder(kwargs['foodstuffid'])
					chef_id			= JSONDecoder(kwargs['chefid'])
					setup 			= SetupFoodBasket(user_id, foodstuff_id)
					res 			= setup.push_foodbasket(chef_id)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodBasketRes(status=res['status'], path=res['path'])

class UpdateQuantiti(grap.Mutation):

	class Arguments:
		foodstrid		= grap.ID()
		basketid		= grap.ID()
		userid 			= grap.ID()
		chefid			= grap.ID()
		quantiti 		= grap.String()

	Output	= SetupFoodBasketRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = res = {'status': False, 'path': 'quantiti'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['basketid']) and len(kwargs['foodstrid']) != 0:
					if len(kwargs['quantiti']) != 0:
						user_id 	= JSONDecoder(kwargs['userid'])
						chef_id 	= JSONDecoder(kwargs['chefid'])
						basket_id	= JSONDecoder(kwargs['basketid'])
						foodstr_id	= kwargs['foodstrid']
						quantiti 	= kwargs['quantiti']
						setup 		= SetupFoodBasket(user_id, None, basket_id)
						res 		= setup.update_quantiti(chef_id, foodstr_id, quantiti)
						return res
					else:
						return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodBasketRes(status=res['status'], path=res['path'])

class PullFooditem(grap.Mutation):

	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		basketid 		= grap.ID()
		foodstrid 		= grap.ID()

	Output 	= SetupFoodBasketRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'pull_fooditem'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['basketid']) != 0:
				if len(kwargs['chefid']) and len(kwargs['foodstrid']) != 0:
					user_id 		= JSONDecoder(kwargs['userid'])
					chef_id			= JSONDecoder(kwargs['chefid'])
					basket_id 		= JSONDecoder(kwargs['basketid'])
					foodstr_id		= kwargs['foodstrid']
					setup 			= SetupFoodBasket(user_id, None, basket_id)
					res 			= setup.pull_fooditem(chef_id, foodstr_id)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodBasketRes(status=res['status'], path=res['path'])

class PullFoodchef(grap.Mutation):

	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		basketid 		= grap.ID()

	Output 	= SetupFoodBasketRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'pull_foodchef'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['basketid']):
				if len(kwargs['chefid']) != 0:
					user_id		= JSONDecoder(kwargs['userid'])
					chef_id 	= JSONDecoder(kwargs['chefid'])
					basket_id 	= JSONDecoder(kwargs['basketid'])
					setup 		= SetupFoodBasket(user_id, None, basket_id)
					res 		= setup.pull_foodchef(chef_id)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodBasketRes(status['status'], path=res['path'])
