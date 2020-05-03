import graphene as grap

from app.api.queries.user.qu_user import UserQueri

from app.api.service.user import UserServ
from app.api.service.chef import ChefServ
from app.api.service.attribute import AttrServ

class Query(UserQueri, grap.ObjectType):
    pass

class Service(UserServ,AttrServ,ChefServ, grap.ObjectType):
    pass

schema = grap.Schema(query=Query, mutation=Service)