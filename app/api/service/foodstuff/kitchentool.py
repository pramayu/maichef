import graphene as grap
from app.model.foodstuff import SetupFoodstuff
from app.api.sekema.foodstuff.sk_foodstuff import SetupFoodstuffRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder


class PushKitchentool(grap.Mutation):

	class Arguments:
		userid 			= grap.ID()
		chefid			= grap.ID()
		foodstuffid		= grap.ID()
		kitchentool 	= grap.List(grap.ID)

	Output	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'kitchentool' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['foodstuffid']) and len(kwargs['kitchentool']) != 0:
					user_id 		= JSONDecoder(kwargs['userid'])
					chef_id 		= JSONDecoder(kwargs['chefid'])
					foodstuff_id	= JSONDecoder(kwargs['foodstuffid'])
					kitchentool 	= map(lambda x: JSONDecoder(x), kwargs['kitchentool'])
					setup 			= SetupFoodstuff(user_id, chef_id, foodstuff_id)
					res 			= setup.push_kitchentool(list(kitchentool))
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])

class PullKitchentool(grap.Mutation):
	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		foodstuffid 	= grap.ID()
		kitchentoolid 	= grap.ID()


	Output 	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'kitchentool' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['foodstuffid']) and len(kwargs['kitchentoolid']) != 0:
					user_id 		= JSONDecoder(kwargs['userid'])
					chef_id			= JSONDecoder(kwargs['chefid'])
					foodstuff_id	= JSONDecoder(kwargs['foodstuffid'])
					kitchentool_id	= JSONDecoder(kwargs['kitchentoolid'])
					setup 			= SetupFoodstuff(user_id, chef_id, foodstuff_id)
					res 			= setup.pull_kitchentool(kitchentool_id)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])