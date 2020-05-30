import graphene as grap

class SetupFoodorderRes(grap.ObjectType):
	path		= grap.String()
	status		= grap.Boolean()
	message		= grap.String()