import graphene as grap
from app.model.occupation import SetupOccupation
from app.common.middleware.authorized import requireauth
from app.api.sekema.attribute.sk_occupation import SetupOccupRes


class PushOccupation(grap.Mutation):
	class Arguments:
		userid			= grap.ID()
		occupation 		= grap.String()


	Output 	= SetupOccupRes


	@requireauth 
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'occupation'}
		if payload['isAuth'] == True:
			userid 		= kwargs['userid']
			occupation 	= kwargs['occupation']
			if len(userid) and len(occupation) != 0:
				try:
					setup 	= SetupOccupation(occupation)
					res 	= setup.insert_occupation()
					return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res
		return SetupOccupRes(status=res['status'], path=res['path'])


class EditOccupation(grap.Mutation):
	class Arguments:
		userid			= grap.ID()
		slug			= grap.String()
		occupation 		= grap.String()

	Output	= SetupOccupRes

	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = {'status': False, 'path': 'occupation'}
		if payload['isAuth'] == True:
			slug 		= kwargs['slug']
			occupation 	= kwargs['occupation']
			if len(slug) and len(occupation) != 0:
				setup = SetupOccupation(occupation)
				res = setup.update_occupation(slug)
				return res
			else:
				return res
		else:
			return res
		return SetupOccupRes(status=res['status'], path=res['path'])