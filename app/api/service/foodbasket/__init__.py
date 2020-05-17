import graphene as grap
from app.api.service.foodbasket.build_basket import BuildFoodBasket
from app.api.service.foodbasket.pushfoodbasket import PushFoodBasket
from app.api.service.foodbasket.pushfoodbasket import UpdateQuantiti
from app.api.service.foodbasket.pushfoodbasket import PullFooditem

class BasketServ(grap.ObjectType):
	buildfoodbasket 		= BuildFoodBasket.Field()
	pushfoodbasket 			= PushFoodBasket.Field()
	updatequantiti 			= UpdateQuantiti.Field()
	pullfooditem 			= PullFooditem.Field()