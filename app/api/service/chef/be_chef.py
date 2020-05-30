import graphene as grap
from app.model.chef import SetupChef
from datetime import datetime, timedelta
from app.common.middleware.JSONDecoder import JSONDecoder
from app.api.sekema.chef.sk_chef import SetupChefRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.buildtoken import buildtoken


class ToBeChef(grap.Mutation):
	class Arguments:
		userid			= grap.ID()

	Output	= SetupChefRes

	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path':'chef', 'accessetoken':None }
		if payload['isAuth'] == True:
			userid 	= JSONDecoder(kwargs['userid'])
			setup 	= SetupChef(userid)
			res 	= setup.be_chef()
			if res['status'] == True:
				payload = {
					'id'		: payload['user_id'],
					'username'	: payload['username'],
					'chef'		: str(res['chef']['id']),
					'exp'		: datetime.utcnow() + timedelta(days=5)
				}
				accessetoken = buildtoken(payload)
				res = { 'status': True, 'path':'chef', 'accessetoken':accessetoken }
				return res
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'], path=res['path'], accessetoken=res['accessetoken'])