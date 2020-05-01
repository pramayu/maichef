import graphene as grap
from app.model.user import SetupUser
from datetime import datetime, timedelta
from app.api.sekema.user.sk_user import SetupUserRes
from app.common.middleware.buildtoken import buildtoken


class ActiveUser(grap.Mutation):
	class Arguments:
		uniqpin		= grap.String()

	Output	= SetupUserRes

	def mutate(self, info, **kwargs):
		uniqpin = kwargs['uniqpin']
		setup = SetupUser()
		res = setup.useractive(uniqpin)
		if res['status'] == True:
			payload = {
				'id'		: str(res['user']['id']),
				'username'	: res['user']['username'],
				'exp'		: datetime.utcnow() + timedelta(days=2)
			}
			if payload:
				refreshtoken = buildtoken(payload)
				return SetupUserRes(status=True, path="activeuser", refreshtoken=refreshtoken)
			else:
				return SetupUserRes(status=False, path="activeuser")
		else:
			return SetupUserRes(status=res['status'], path=res['path'])