import graphene as grap
from app.model.user import SetupUser
from app.api.sekema.user.sk_user import SetupUserRes


class SignupUser(grap.Mutation):
	class Arguments:
		username	= grap.String()
		email		= grap.String()
		password	= grap.String()

	Output	= SetupUserRes

	def mutate(self, info, **kwargs):
		username = kwargs['username']
		password = kwargs['password'].encode('utf-8')
		email = kwargs['email']
		setup = SetupUser()
		res = setup.insertuser(username, password, email)
		return SetupUserRes(status=res['status'], path=res['path'])