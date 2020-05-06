import graphene as grap
from app.api.sekema.user.sk_user import UserSkema

class UserQueri(grap.ObjectType):
	user 	= grap.List(UserSkema)

	def resolve(root, info):
		pass