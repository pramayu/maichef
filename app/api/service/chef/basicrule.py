import graphene as grap
from app.model.chef import SetupChef
from app.api.sekema.chef.sk_chef import SetupChefRes
from app.common.middleware.JSONDecoder import JSONDecoder
from app.common.middleware.authorized import requireauth


class StoreBasicRule(grap.Mutation):
	class Arguments:
		userid			= grap.ID()
		chefid			= grap.ID()
		limittask		= grap.String()
		rangework		= grap.String()
		rules			= grap.List(grap.String)

	Output 	= SetupChefRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path':'rule' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['limittask']) != 0:
					user_id			= JSONDecoder(kwargs['userid'])
					chef_id			= JSONDecoder(kwargs['chefid'])
					limit_task		= kwargs['limittask']
					range_work 		= kwargs['rangework']
					rules			= kwargs['rules']
					setup 			= SetupChef(user_id, chef_id)
					res 			= setup.store_basic_rule(limit_task,range_work,rules)
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'], path=res['path'])

class UpdatBasicRule(grap.Mutation):
	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		limittask 		= grap.String()
		rangework 		= grap.String()
		rules 			= grap.List(grap.String)
		strid 			= grap.ID()

	Output 	= SetupChefRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path':'rule' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['limittask']) and len(kwargs['strid']) != 0:
					user_id		= JSONDecoder(kwargs['userid'])
					chef_id 	= JSONDecoder(kwargs['chefid'])
					str_id		= kwargs['strid']
					range_work 	= kwargs['rangework']
					limit_task	= kwargs['limittask']
					rules		= kwargs['rules']
					setup 		= SetupChef(user_id, chef_id, str_id)
					res 		= setup.update_basic_rule(limit_task,range_work,rules)
					return res
				else:
					return res	
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'], path=res['path'])