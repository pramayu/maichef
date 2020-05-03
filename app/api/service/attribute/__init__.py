import graphene as grap
from app.api.service.attribute.occupation import PushOccupation, EditOccupation


class AttrServ(grap.ObjectType):
	pushoccupation			= PushOccupation.Field()
	editoccupation 			= EditOccupation.Field()