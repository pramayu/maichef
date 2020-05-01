import jwt
import graphene 							as grap
from datetime								import datetime, timedelta
from app.model.user 						import SetupUser
from app.model.blacklist 					import BlacklistSetup
from app.api.sekema.user.sk_user 			import SetupUserRes
from app.common.middleware.buildtoken 		import checktoken, buildtoken
from app.common.middleware.JSONDecoder 		import JSONDecoder
from app.common.middleware.BSONObjctid 		import BSONObjctid


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
						setup 	= SetupUser()
						res 	= setup.checkusertoken(xreftoken['id'])
						paylaod = {
							'id'		: str(res['user']['id']),
							'username'	: res['user']['username'],
							'exp'		: datetime.utcnow() + timedelta(days=5)
						}
						if paylaod:
							accessetoken = buildtoken(paylaod)
							return SetupUserRes(status=True, path="checkuser",
												accessetoken=accessetoken)
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