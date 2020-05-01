import graphene as grap
from app.api.service.user.signup import SignupUser
from app.api.service.user.activeuser import ActiveUser
from app.api.service.user.checkuser import CheckUserToken

class UserServ(grap.ObjectType):
	signupuser 			= SignupUser.Field()
	activeuser 			= ActiveUser.Field()
	checkusertoken 		= CheckUserToken.Field()