import graphene as grap
from app.api.service.user.signup import SignupUser
from app.api.service.user.activeuser import ActiveUser

class UserServ(grap.ObjectType):
	signupuser 	= SignupUser.Field()
	activeuser 	= ActiveUser.Field()