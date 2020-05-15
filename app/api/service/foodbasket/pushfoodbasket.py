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
