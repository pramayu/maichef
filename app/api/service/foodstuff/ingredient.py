import graphene as grap
from app.model.foodstuff import SetupFoodstuff
from app.api.sekema.foodstuff.sk_foodstuff import SetupFoodstuffRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder


class PushIngredient(grap.Mutation):

	class Arguments:
		userid 		= grap.ID()
		chefid		= grap.ID()
		ingredient 	= grap.List(grap.String)
		foodstuffid	= grap.ID()

	Output	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'ingredient' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['ingredient']) and len(kwargs['foodstuffid']) != 0:
					user_id			= JSONDecoder(kwargs['userid'])
					chef_id			= JSONDecoder(kwargs['chefid'])
					foodstuff_id	= JSONDecoder(kwargs['foodstuffid'])
					ingredient 		= kwargs['ingredient']
					setup 			= SetupFoodstuff(user_id, chef_id,foodstuff_id)
					res 			= setup.push_ingredient(ingredient)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])

class PullIngredient(grap.Mutation):

	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		strid 			= grap.ID()
		foodstuffid 	= grap.ID()

	Output	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'ingredient' }
		if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
			if len(kwargs['strid']) and len(kwargs['foodstuffid']) != 0:
				user_id			= JSONDecoder(kwargs['userid'])
				chef_id			= JSONDecoder(kwargs['chefid'])
				foodstuff_id	= JSONDecoder(kwargs['foodstuffid'])
				str_id			= kwargs['strid']
				setup 			= SetupFoodstuff(user_id, chef_id, foodstuff_id, str_id)
				res 			= setup.pull_ingredient()
				return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])