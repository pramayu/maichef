import graphene as grap
from app.api.service.foodbasket.build_basket import BuildFoodBasket
from app.api.service.foodbasket.pushfoodbasket import PushFoodBasket
from app.api.service.foodbasket.pushfoodbasket import UpdateQuantiti
from app.api.service.foodbasket.pushfoodbasket import PullFooditem
from app.api.service.foodbasket.pushfoodbasket import PullFoodchef
from app.api.service.foodbasket.pushfoodbasket import PushKitchenstuff
from app.api.service.foodbasket.pushfoodbasket import PullKitchentool
from app.api.service.foodbasket.pushfoodbasket import WhoBoughtInggr

class BasketServ(grap.ObjectType):
	pushfoodbasket 			= PushFoodBasket.Field()
	updatequantiti 			= UpdateQuantiti.Field()
	pullfooditem 			= PullFooditem.Field()
	pullfoodchef 			= PullFoodchef.Field()
	buildfoodbasket 		= BuildFoodBasket.Field()
	pushkitchenstuff 		= PushKitchenstuff.Field()
	pullkitchenstuff 		= PullKitchentool.Field()
	whoboughtinggr 			= WhoBoughtInggr.Field()