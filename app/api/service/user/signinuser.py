import graphene as grap
from app.model.user import SetupUser
from datetime import datetime, timedelta
from app.api.sekema.user.sk_user import SetupUserRes
from app.common.middleware.buildtoken import buildtoken


class SigninUser(grap.Mutation):
	class Arguments:
		identity		= grap.String()
		password		= grap.String()


	Output	= SetupUserRes


	def mutate(self, info, **kwargs):
		if len(kwargs['identity']) and len(kwargs['password']) != 0:
			identity = kwargs['identity']
			password = kwargs['password'].encode('utf-8')
			setup = SetupUser()
			res = setup.identityuser(identity, password)
			if res['status'] == True:
				payload = {
					'id'		: str(res['user']['id']),
					'username'	: res['user']['username'],
					'exp'		: datetime.utcnow() + timedelta(days=2)
				}
				if payload:
					token = buildtoken(payload)
					return SetupUserRes(status=True, path="identityuser", refreshtoken=token)
				else:
					return SetupUserRes(status=False, path="identityuser")
			else:
				return SetupUserRes(status=False, path="identityuser")
		else:
			return SetupUserRes(status=False, path="identityuser")