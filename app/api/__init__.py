import graphene as grap

from app.api.queri.user.qu_user import UserQueri

from app.api.service.user import UserServ

class Query(UserQueri, grap.ObjectType):
    pass

class Service(UserServ, grap.ObjectType):
    pass

schema = grap.Schema(query=Query, mutation=Service)