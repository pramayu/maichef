import graphene as grap
from app.model.user import SetupUser
from app.api.sekema.user.sk_user import SetupUserRes


class ActiveUser(grap.Mutation):
	class Arguments:
		uniqpin		= grap.String()

	Output	= SetupUserRes

	def mutate(self, info, **kwargs):
		uniqpin = kwargs['uniqpin']
		setup = SetupUser()
		res = setup.useractive(uniqpin)
		return SetupUserRes(status=res['status'], path=res['path'])