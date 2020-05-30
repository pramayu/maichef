import graphene as grap
from app.api.service.foodorder.req_userorder import RequestFoodOrder

class FoodorderServ(grap.ObjectType):
	requserorder 			= RequestFoodOrder.Field()