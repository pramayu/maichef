import graphene as grap

class SetupChefRes(grap.ObjectType):
	path			= grap.String()
	status			= grap.Boolean()
	message			= grap.String()
	accessetoken	= grap.String()