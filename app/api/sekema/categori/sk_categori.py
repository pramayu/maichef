import graphene as grap

class SetupCategoriRes(grap.ObjectType):
	path		= grap.String()
	status		= grap.Boolean()
	message		= grap.String()