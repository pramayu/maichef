import graphene as grap
from app.api.service.foodbasket.build_basket import BuildFoodBasket

class BasketServ(grap.ObjectType):
	buildfoodbasket 		= BuildFoodBasket.Field()
