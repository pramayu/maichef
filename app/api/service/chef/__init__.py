import graphene as grap
from app.api.service.chef.be_chef import ToBeChef
from app.api.service.chef.experience import PushExperience
from app.api.service.chef.experience import EditExperience

class ChefServ(grap.ObjectType):
	tobechef 			= ToBeChef.Field()
	pushexperience 		= PushExperience.Field()
	editexperience 		= EditExperience.Field()
