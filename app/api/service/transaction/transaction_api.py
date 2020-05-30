import graphene as grap
from app.model.transaction import SetupTransaction
from app.api.sekema.transaction.sk_transaction import SetupTransactionRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder


class RequestPaymentCharge(grap.Mutation):
	class Arguments:
		userid			= grap.ID()
		orderid			= grap.ID()

	Output	= SetupTransactionRes

	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'transaction'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['orderid']):
				user_id			= JSONDecoder(kwargs['userid'])
				order_id		= JSONDecoder(kwargs['orderid'])
				setup 			= SetupTransaction(user_id)
				res 			= setup.request_transaction(order_id)
				return res
			else:
				return res
		else:
			return res
		return SetupTransactionRes(status=res['status'], path=res['path'])