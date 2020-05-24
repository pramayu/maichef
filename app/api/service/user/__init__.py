import graphene as grap
from app.api.service.user.signupuser import SignupUser
from app.api.service.user.checkuser import CheckUserToken
from app.api.service.user.activeuser import ActiveUser
from app.api.service.user.signinuser import SigninUser
from app.api.service.user.useraddress import PushUserAddress
from app.api.service.user.useraddress import PullUserAddress
from app.api.service.user.useraddress import UpdateUserAddress
from app.api.service.user.useraddress import ChooseUserAddress

class UserServ(grap.ObjectType):
	signupuser 			= SignupUser.Field()
	activeuser 			= ActiveUser.Field()
	checkusertoken 		= CheckUserToken.Field()
	signinuser 			= SigninUser.Field()
	pushuseraddress 	= PushUserAddress.Field()
	pulluseraddress		= PullUserAddress.Field()
	updateuseraddress 	= UpdateUserAddress.Field()
	chooseuseraddress 	= ChooseUserAddress.Field()