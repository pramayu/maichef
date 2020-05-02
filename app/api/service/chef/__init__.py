import graphene as grap
from app.api.service.chef.be_chef import ToBeChef

class ChefServ(grap.ObjectType):
	tobechef 			= ToBeChef.Field()