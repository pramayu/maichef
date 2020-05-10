import graphene as grap
from app.api.service.foodstuff.sharefood import InsertFoodStuff
from app.api.service.foodstuff.sharefood import UpdateFoodStuff
from app.api.service.foodstuff.sharefood import UpdateFoodCategori
from app.api.service.foodstuff.sharefood import PullFoodCategori
from app.api.service.foodstuff.ingredient import PushIngredient
from app.api.service.foodstuff.ingredient import PullIngredient
from app.api.service.foodstuff.kitchentool import PushKitchentool
from app.api.service.foodstuff.kitchentool import PullKitchentool


class FoodServ(grap.ObjectType):
	insertfoodstuff 		= InsertFoodStuff.Field()
	updatefoodstuff 		= UpdateFoodStuff.Field()
	updatefoodcategori 		= UpdateFoodCategori.Field()
	pullfoodcategori 		= PullFoodCategori.Field()
	pushingredient 			= PushIngredient.Field()
	pullingredient 			= PullIngredient.Field()
	pushkitchentool 		= PushKitchentool.Field()
	pullkitchentool 		= PullKitchentool.Field()