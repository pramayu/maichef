import graphene as grap

from app.api.queries.user.qu_user import UserQueri

from app.api.service.user import UserServ
from app.api.service.chef import ChefServ
from app.api.service.foodstuff import FoodServ
from app.api.service.attribute import AttrServ
from app.api.service.foodbasket import BasketServ
from app.api.service.schedule import ScheduleServ
from app.api.service.foodorder import FoodorderServ
from app.api.service.transaction import TranServ

class Query(UserQueri, grap.ObjectType):
    pass

class Service(UserServ,AttrServ,ChefServ,FoodServ,BasketServ,ScheduleServ,FoodorderServ,TranServ, grap.ObjectType):
    pass

schema = grap.Schema(query=Query, mutation=Service)