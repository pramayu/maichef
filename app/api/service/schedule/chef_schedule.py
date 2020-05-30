import graphene as grap
from app.model.schedule import SetupChefSchedule
from app.api.sekema.schedule.sk_schedule import SetupChefScheduleRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder
from app.common.chk_input.schedule import chk_datime


class PushChefSchedule(grap.Mutation):
	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		datime			= grap.String()

	Output 	= SetupChefScheduleRes

	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'push_chef_schedule'}
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['datime']) != 0:
					rs = chk_datime(kwargs['datime'])
					if rs:
						user_id 	= JSONDecoder(kwargs['userid'])
						chef_id		= JSONDecoder(kwargs['chefid'])
						setup 		= SetupChefSchedule(user_id, chef_id)
						res 		= setup.modif_chef_schedule(rs)
						return res
					else:
						return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupChefScheduleRes(status=res['status'], path=res['path'])