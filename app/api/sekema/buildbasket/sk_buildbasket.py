import graphene as grap


class SetupFoodBasketRes(grap.ObjectType):
	path 		= grap.String()
	status 		= grap.Boolean()
	message 	= grap.String()