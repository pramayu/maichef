import graphene as grap

from app.api.service.schedule.chef_schedule import PushChefSchedule

class ScheduleServ(grap.ObjectType):
	pushchefschedule 		= PushChefSchedule.Field()