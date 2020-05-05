import graphene as grap
from app.model.chef import SetupChef
from app.common.middleware.JSONDecoder import JSONDecoder
from app.common.middleware.authorized import requireauth
from app.api.sekema.chef.sk_chef import SetupChefRes


class PushServiceArea(grap.Mutation):
	class Arguments:
		userid			= grap.ID()
		chefid			= grap.ID()
		area 			= grap.String()

	Output 	= SetupChefRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'servicearea' }
		if payload['isAuth'] == True:
			if len(kwargs['chefid']) and len(kwargs['area']) != 0:
				user_id 		= JSONDecoder(kwargs['userid'])
				chef_id 		= JSONDecoder(kwargs['chefid'])
				service_area 	= kwargs['area']
				setup 			= SetupChef(user_id, chef_id)
				res 			= setup.push_service_area(service_area)
				return res
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'], path=res['path'])

class PullServiceArea(grap.Mutation):
	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		strid 			= grap.ID()

	Output	= SetupChefRes

	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'servicearea' }
		if payload['isAuth'] == True:
			if len(kwargs['chefid']) and len(kwargs['strid']) != 0:
				user_id		= JSONDecoder(kwargs['userid'])
				chef_id		= JSONDecoder(kwargs['chefid'])
				str_id		= kwargs['strid']
				setup 		= SetupChef(user_id, chef_id, str_id)
				res 		= setup.pull_service_area()
				return res
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'], path=res['path'])