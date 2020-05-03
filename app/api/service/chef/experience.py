import graphene as grap
from datetime import datetime
from app.model.chef import SetupChef
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder
from app.api.sekema.chef.sk_chef import SetupChefRes


class PushExperience(grap.Mutation):
	class Arguments:
		chefid			= grap.ID()
		userid			= grap.ID()
		occupation		= grap.ID()
		lengthofwork	= grap.List(grap.String)
		workplace		= grap.String()

	Output	= SetupChefRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'experience' }
		if payload['isAuth'] == True:
			if len(kwargs['chefid']) != 0:
				occupation 		= JSONDecoder(kwargs['occupation'])
				chef_id			= JSONDecoder(kwargs['chefid'])
				user_id			= JSONDecoder(kwargs['userid'])
				length_of_work 	= kwargs['lengthofwork']
				work_place		= kwargs['workplace']
				setup 			= SetupChef(user_id, chef_id)
				res 			= setup.push_experience(occupation, length_of_work, work_place)
				return res
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'], path=res['path'])

class EditExperience(grap.Mutation):
	class Arguments:
		strid			= grap.ID()
		chefid			= grap.ID()
		userid			= grap.ID()
		occupation		= grap.ID()
		lengthofwork	= grap.List(grap.String)
		workplace		= grap.String()

	Output	= SetupChefRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'experience' }
		if payload['isAuth'] == True:
			if len(kwargs['chefid']) and len(kwargs['strid']) != 0:
				strid			= kwargs['strid']
				chef_id			= JSONDecoder(kwargs['chefid'])
				user_id			= JSONDecoder(kwargs['userid'])
				occupation		= JSONDecoder(kwargs['occupation'])
				length_of_work	= kwargs['lengthofwork']
				work_place		= kwargs['workplace']
				setup 			= SetupChef(user_id, chef_id, strid)
				res 			= setup.edit_experience(occupation, length_of_work, work_place)
				return res
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'], path=res['path'])


class PullExperience(grap.Mutation):
	class Arguments:
		userid 			= grap.ID()
		strid 			= grap.ID()
		chefid 			= grap.ID()

	Output	= SetupChefRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'experience' }
		if payload['isAuth'] == True:
			if len(kwargs['chefid']) and len(kwargs['strid']) != 0:
				user_id		= JSONDecoder(kwargs['userid'])
				strid		= kwargs['strid']
				chef_id		= JSONDecoder(kwargs['chefid'])
				setup 		= SetupChef(user_id, chef_id, strid)
				res 		= setup.pull_experience()
				return res
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'], path=res['path'])