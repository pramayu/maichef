import graphene as grap
from app.model.foodbasket import SetupFoodBasket
from app.api.sekema.buildbasket.sk_buildbasket import SetupFoodBasketRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder


class RequestSchedule(grap.Mutation):
	class Arguments:
		userid			= grap.ID()
		chefid 			= grap.ID()
		rqdate			= grap.String()
		rqtime			= grap.String()
		basketid		= grap.ID()

	Output 	= SetupFoodBasketRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'req_schedule'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['basketid']) != 0:
				if len(kwargs['chefid']) and len(kwargs['rqtime']) and len(kwargs['rqdate']) != 0:
					user_id 		= JSONDecoder(kwargs['userid'])
					chef_id 		= JSONDecoder(kwargs['chefid'])
					basket_id		= JSONDecoder(kwargs['basketid'])
					rq_date 		= kwargs['rqdate']
					rq_time 		= f"{kwargs['rqtime']}:00"
					setup 			= SetupFoodBasket(user_id, None, basket_id)
					res 			= setup.request_schedule(chef_id, rq_date, rq_time)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodBasketRes(status=res['status'], path=res['path'])

