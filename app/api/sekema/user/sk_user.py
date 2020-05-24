import graphene as grap

class UserSkema(grap.ObjectType):
    id             	= grap.ID()
    username        = grap.String()
    emailadd        = grap.String()
    activate        = grap.Boolean()


class SetupUserRes(grap.ObjectType):
	path			= grap.String()
	status			= grap.Boolean()
	refreshtoken	= grap.String()
	accessetoken	= grap.String()

class SetupUserAttributeRes(grap.ObjectType):
	path			= grap.String()
	status			= grap.Boolean()
	message 		= grap.String()