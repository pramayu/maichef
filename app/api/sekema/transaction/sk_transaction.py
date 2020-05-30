import graphene as grap


class SetupTransactionRes(grap.ObjectType):
	path		= grap.String()
	status		= grap.Boolean()
	message		= grap.String()