import jwt
import graphene as grap
from app.model.user import SetupUser
from app.model.chef import SetupChef
from datetime import datetime, timedelta
from app.model.blacklist import BlacklistSetup
from app.api.sekema.user.sk_user import SetupUserRes
from app.common.middleware.buildtoken import checktoken, buildtoken


class CheckUserToken(grap.Mutation):
	class Arguments:
		refreshtoken	= grap.String()

	Output	= SetupUserRes


	def mutate(self, info, **kwargs):
		if len(kwargs['refreshtoken']) != 0:
			refreshtoken = kwargs['refreshtoken']
			bltoken = BlacklistSetup(refreshtoken)
			res = bltoken.checktoken()
			if res['status'] == False:
				try:
					xreftoken	= checktoken(refreshtoken)
					if xreftoken:
						_setup 	= SetupUser()
						_res 	= _setup.checkusertoken(xreftoken['id'])
						setup_	= SetupChef(_res['user']['id'])
						res_	= setup_.chk_chef()
						paylaod = {
							'id'		: str(_res['user']['id']),
							'username'	: _res['user']['username'],
							'exp'		: datetime.utcnow() + timedelta(days=5),
							'chef'		: str(res_['chef']['id']) if res_['status'] == True else ""
						}
						if paylaod:
							accessetoken = buildtoken(paylaod)
							return SetupUserRes(status=True, path="checkuser", accessetoken=accessetoken)
						else:
							return SetupUserRes(status=False, path="checkuser")
					else:
						return SetupUserRes(status=False, path="checkuser")
				except jwt.ExpiredSignatureError:
					bltoken.inserttoken()
					return SetupUserRes(status=False, path="checkuser")
			else:
				return SetupUserRes(status=False, path="checkuser")
		else:
			return SetupUserRes(status=False, path="checkuser")