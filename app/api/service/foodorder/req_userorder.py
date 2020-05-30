import graphene as grap
from app.model.foodorder import SetupFoodorder
from app.api.sekema.foodorder.sk_foodorder import SetupFoodorderRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder



class RequestFoodOrder(grap.Mutation):

	class Arguments:
		userid 			= grap.ID()
		addrid			= grap.ID()
		basketid		= grap.ID()

	Output	= SetupFoodorderRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path':'req_foodorder'}
		print(payload)
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['basketid']) != 0:
				if len(kwargs['addrid']) != 0:
					user_id			= JSONDecoder(kwargs['userid'])
					addr_id			= JSONDecoder(kwargs['addrid'])
					basket_id		= JSONDecoder(kwargs['basketid'])
					setup 			= SetupFoodorder(user_id, basket_id, addr_id)
					res 			= setup.create_order()
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodorderRes(status=res['status'], path=res['path'])