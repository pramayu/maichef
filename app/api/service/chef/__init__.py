import graphene as grap
from app.api.service.chef.be_chef import ToBeChef
from app.api.service.chef.experience import PushExperience
from app.api.service.chef.experience import EditExperience
from app.api.service.chef.experience import PullExperience
from app.api.service.chef.honour import PushHonour
from app.api.service.chef.honour import PullHonour
from app.api.service.chef.servicearea import PushServiceArea
from app.api.service.chef.servicearea import PullServiceArea

class ChefServ(grap.ObjectType):
	tobechef 			= ToBeChef.Field()
	pushexperience 		= PushExperience.Field()
	editexperience 		= EditExperience.Field()
	pullexperience 		= PullExperience.Field()
	pushhonour 			= PushHonour.Field()
	pullhonour 			= PullHonour.Field()
	pushservicearea		= PushServiceArea.Field()
	pullservicearea 	= PullServiceArea.Field()
