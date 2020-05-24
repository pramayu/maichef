import graphene as grap
from app.model.user import SetupUserAttribute
from app.api.sekema.user.sk_user import SetupUserAttributeRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder


class PushUserAddress(grap.Mutation):
	class Arguments:
		userid 			= grap.ID()
		regenci 		= grap.String()
		province		= grap.String()
		street 			= grap.String()
		point 			= grap.List(grap.Float)

	Output 	= SetupUserAttributeRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'push_user_address'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['point']) != 0:
				if len(kwargs['province']) and len(kwargs['regenci']) != 0:
					if len(kwargs['street']) != 0:
						user_id 		= JSONDecoder(kwargs['userid'])
						attr 			= {
							'province'		: kwargs['province'],
							'regenci'		: kwargs['regenci'],
							'street'		: kwargs['street'],
							'point'			: kwargs['point']
						}
						setup 			= SetupUserAttribute(user_id, None)
						res 			= setup.push_user_address(attr)
						return res
					else:
						return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupUserAttributeRes(status=res['status'], path=res['path'])

class UpdateUserAddress(grap.Mutation):
	class Arguments:
		userid 			= grap.ID()
		addrid 			= grap.ID()
		regenci 		= grap.String()
		province		= grap.String()
		street 			= grap.String()
		point 			= grap.List(grap.Float)

	Output	= SetupUserAttributeRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'update_user_address'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['addrid']) != 0:
				if len(kwargs['regenci']) and len(kwargs['province']) != 0:
					if len(kwargs['street']) and len(kwargs['point']) != 0:
						user_id 		= JSONDecoder(kwargs['userid'])
						addr_id			= JSONDecoder(kwargs['addrid'])
						attr 			= {
							'province'		: kwargs['province'],
							'regenci'		: kwargs['regenci'],
							'street'		: kwargs['street'],
							'point'			: kwargs['point']
						}
						setup 			= SetupUserAttribute(user_id, addr_id)
						res 			= setup.update_user_address(attr)
						return res
					else:
						return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupUserAttributeRes(status=res['status'], path=res['path'])

class PullUserAddress(grap.Mutation):
	class Arguments:
		userid 			= grap.ID()
		addrid 			= grap.ID()

	Output 	= SetupUserAttributeRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'pull_user_address'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['addrid']) != 0:
				user_id 		= JSONDecoder(kwargs['userid'])
				addr_id 		= JSONDecoder(kwargs['addrid'])
				setup 			= SetupUserAttribute(user_id, addr_id)
				res 			= setup.pull_user_address()
				return res
			else:
				return res
		else:
			return res
		return SetupUserAttributeRes(status=res['status'], path=res['path'])

class ChooseUserAddress(grap.Mutation):
	class Arguments:
		userid 			= grap.ID()
		addrid 			= grap.ID()

	Output 	= SetupUserAttributeRes

	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'choose_user_address'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['addrid']) != 0:
				user_id 		= JSONDecoder(kwargs['userid'])
				addr_id 		= JSONDecoder(kwargs['addrid'])
				setup 			= SetupUserAttribute(user_id, addr_id)
				res 			= setup.choose_user_address()
				return res
			else:
				return res
		else:
			return res
		return SetupUserAttributeRes(status=res['status'], path=res['path'])