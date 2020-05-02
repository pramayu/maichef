import graphene as grap
from app.api.service.attribute.occupation import PushOccupation, EditOccupation


class AttributeServ(grap.ObjectType):
	pushoccupation			= PushOccupation.Field()
	editoccupation 			= EditOccupation.Field()