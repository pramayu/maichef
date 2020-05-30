import graphene as grap

class SetupFoodstuffRes(grap.ObjectType):
	path		= grap.String()
	status		= grap.Boolean()
	message		= grap.String()