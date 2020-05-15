import graphene as grap
from app.api.service.foodbasket.build_basket import BuildFoodBasket
from app.api.service.foodbasket.pushfoodbasket import PushFoodBasket

class BasketServ(grap.ObjectType):
	buildfoodbasket 		= BuildFoodBasket.Field()
	pushfoodbasket 			= PushFoodBasket.Field()