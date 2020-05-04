import graphene as grap
from app.model.chef import SetupChef
from app.api.sekema.chef.sk_chef import SetupChefRes
from app.common.middleware.JSONDecoder import JSONDecoder
from app.common.middleware.authorized import requireauth


class PushHonour(grap.Mutation):
	class Arguments:
		userid			= grap.ID()
		chefid			= grap.ID()
		instit			= grap.String()
		yearhonour		= grap.String()
		infield			= grap.String()


	Output	= SetupChefRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path':'honour'}
		if payload['isAuth'] == True:
			if len(kwargs['chefid']) and len(kwargs['userid']) != 0:
				user_id			= JSONDecoder(kwargs['userid'])
				chef_id			= JSONDecoder(kwargs['chefid'])
				instit			= kwargs['instit']
				year_honour		= kwargs['yearhonour']
				in_the_field	= kwargs['infield']
				if len(instit) and len(year_honour) and len(in_the_field) != 0:
					setup 		= SetupChef(user_id, chef_id)
					res 		= setup.push_honour(instit, year_honour, in_the_field)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'], path=res['path'])

class PullHonour(grap.Mutation):
	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		strid			= grap.ID()

	Output	= SetupChefRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path':'honour'}
		if payload['isAuth'] == True:
			if len(kwargs['strid']) and len(kwargs['chefid']) != 0:
				user_id		= JSONDecoder(kwargs['userid'])
				chef_id		= JSONDecoder(kwargs['chefid'])
				str_id		= kwargs['strid']
				setup 		= SetupChef(user_id, chef_id, str_id)
				res 		= setup.pull_honour()
				return res
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'], path=res['path'])