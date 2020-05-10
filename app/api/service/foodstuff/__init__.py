import graphene as grap
from app.api.service.foodstuff.sharefood import InsertFoodStuff
from app.api.service.foodstuff.sharefood import UpdateFoodStuff
from app.api.service.foodstuff.sharefood import UpdateFoodCategori
from app.api.service.foodstuff.sharefood import PullFoodCategori


class FoodServ(grap.ObjectType):
	insertfoodstuff 		= InsertFoodStuff.Field()
	updatefoodstuff 		= UpdateFoodStuff.Field()
	updatefoodcategori 		= UpdateFoodCategori.Field()
	pullfoodcategori 		= PullFoodCategori.Field()