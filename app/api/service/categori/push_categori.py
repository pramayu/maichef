import graphene as grap
from app.model.categori import SetupCategori
from app.api.sekema.categori.sk_categori import SetupCategoriRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder


class PushCategori(grap.Mutation):
	class Arguments:
		userid		= grap.ID()
		chefid		= grap.ID()
		categori 	= grap.String()

	Output	= SetupCategoriRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'categori' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['categori']) != 0:
					user_id		= JSONDecoder(kwargs['userid'])
					categori 	= kwargs['categori']
					setup 		= SetupCategori(user_id)
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupCategoriRes(status=res['status'], path=res['path'])