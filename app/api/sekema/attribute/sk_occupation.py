import graphene as grap


class OccupationSkema(grap.ObjectType):
	id 			= grap.ID()
	role		= grap.String()
	slug		= grap.String()

class SetupOccupRes(grap.ObjectType):
	path		= grap.String()
	status		= grap.Boolean()
	message		= grap.String()