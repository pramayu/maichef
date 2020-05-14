import graphene as grap
from app.model.foodbasket import SetupFoodBasket
from app.api.sekema.buildbasket.sk_buildbasket import SetupFoodBasketRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder


class BuildFoodBasket(grap.Mutation):

	class Arguments:
		userid		= grap.ID()

	Output 	= SetupFoodBasketRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'build_basket'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) != 0:
				user_id		= JSONDecoder(kwargs['userid'])
				setup 		= SetupFoodBasket(user_id)
				res 		= setup.build_basket()
				return res
			else:
				return res
		else:
			return res
		return SetupFoodBasketRes(status=res['status'], path=res['path'])