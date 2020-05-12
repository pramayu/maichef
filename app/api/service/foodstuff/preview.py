import graphene as grap
from app.model.foodstuff import SetupFoodstuff
from app.api.sekema.foodstuff.sk_foodstuff import SetupFoodstuffRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.JSONDecoder import JSONDecoder
from app.common.middleware.IMGUpload import IMGUploadChef
from app.common.middleware.IMGUpload import IMGDestroiChef


class PushPreview(grap.Mutation):

	class Arguments:
		code64			= grap.String()
		userid			= grap.ID()
		chefid			= grap.ID()
		foodstuffid 	= grap.ID()

	Output	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'preview' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['foodstuffid']) and len(kwargs['code64']) != 0:
					foodstuff_id	= JSONDecoder(kwargs['foodstuffid'])
					user_id 		= JSONDecoder(kwargs['userid'])
					chef_id			= JSONDecoder(kwargs['chefid'])
					code64 			= kwargs['code64']
					imgsetup 		= IMGUploadChef(code64, 320)
					imgres 			= imgsetup.upload()
					if imgres:
						url 		= imgres['eager'][0]['secure_url']
						img_type	= imgres['format']
						public_id 	= imgres['public_id']
						setup 		= SetupFoodstuff(user_id, chef_id, foodstuff_id)
						res 		= setup.push_preview(url, img_type, public_id)
						return res
					else:
						return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])

class LetReusePreview(grap.Mutation):

	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		foodstuffid 	= grap.ID()
		strid 			= grap.ID()

	Output	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'preview' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['foodstuffid']) and len(kwargs['strid']) != 0:
					user_id			= JSONDecoder(kwargs['userid'])
					chef_id 		= JSONDecoder(kwargs['chefid'])
					foodstuff_id 	= JSONDecoder(kwargs['foodstuffid'])
					str_id			= kwargs['strid']
					setup 			= SetupFoodstuff(user_id, chef_id, foodstuff_id, str_id)
					res 			= setup.reuse_preview()
					return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])

class DestroiPreview(grap.Mutation):

	class Arguments:
		userid 			= grap.ID()
		chefid 			= grap.ID()
		foodstuffid 	= grap.ID()
		strid 			= grap.ID()
		publicid 		= grap.String()

	Output 	= SetupFoodstuffRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'preview' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['foodstuffid']) and len(kwargs['strid']) != 0:
					if len(kwargs['publicid']) != 0:
						user_id 		= JSONDecoder(kwargs['userid'])
						chef_id 		= JSONDecoder(kwargs['chefid'])
						foodstuff_id	= JSONDecoder(kwargs['foodstuffid'])
						str_id 			= kwargs['strid']
						setup 			= SetupFoodstuff(user_id, chef_id, foodstuff_id, str_id)
						res 			= setup.preview_destroi()
						if res['status'] == True:
							public_id 		= kwargs['publicid']
							dlsetup 		= IMGDestroiChef(public_id)
							dlres 			= dlsetup.destroi()
							if dlres['result'] == 'ok':
								return res
						else:
							return res
					else:
						return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupFoodstuffRes(status=res['status'], path=res['path'])

