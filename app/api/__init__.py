import graphene as grap

from app.api.queries.user.qu_user import UserQueri

from app.api.service.user import UserServ
from app.api.service.chef import ChefServ
from app.api.service.foodstuff import FoodServ
from app.api.service.attribute import AttrServ
from app.api.service.foodbasket import BasketServ

class Query(UserQueri, grap.ObjectType):
    pass

class Service(UserServ,AttrServ,ChefServ,FoodServ,BasketServ, grap.ObjectType):
    pass

schema = grap.Schema(query=Query, mutation=Service)