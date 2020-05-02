import graphene as grap
from app.api.service.user.signupuser import SignupUser
from app.api.service.user.checkuser import CheckUserToken
from app.api.service.user.activeuser import ActiveUser
from app.api.service.user.signinuser import SigninUser

class UserServ(grap.ObjectType):
	signupuser 			= SignupUser.Field()
	activeuser 			= ActiveUser.Field()
	checkusertoken 		= CheckUserToken.Field()
	signinuser 			= SigninUser.Field()