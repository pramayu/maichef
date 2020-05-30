import graphene as grap


class SetupChefScheduleRes(grap.ObjectType):
	path		= grap.String()
	status 		= grap.Boolean()
	message		= grap.String()