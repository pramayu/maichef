import graphene as grap
from app.model.chef import SetupChef
from app.common.middleware.JSONDecoder import JSONDecoder
from app.api.sekema.chef.sk_chef import SetupChefRes
from app.common.middleware.authorized import requireauth
from app.common.middleware.IMGUpload import IMGUploadChef

class PushPictureChef(grap.Mutation):
	class Arguments:
		code64		= grap.String()
		userid		= grap.ID()
		chefid		= grap.ID()


	Output	= SetupChefRes


	@requireauth
	def mutate(payload, self, info, **kwargs):
		res = { 'status': False, 'path': 'upload' }
		if payload['isAuth'] == True:
			if len(kwargs['userid']) and len(kwargs['chefid']) != 0:
				if len(kwargs['code64']) != 0:
					user_id		= JSONDecoder(kwargs['userid'])
					chef_id		= JSONDecoder(kwargs['chefid'])
					qupload		= IMGUploadChef(kwargs['code64'], 280)
					qresult		= qupload.upload()
					if qresult:
						url			= qresult['eager'][0]['secure_url']
						tipe		= qresult['format']
						publicid	= qresult['public_id']
						setup 		= SetupChef(user_id, chef_id)
						res 		= setup.upload_chef_img(url, tipe, publicid)
						return res
					else:
						return res
				else:
					return res
			else:
				return res
		else:
			return res
		return SetupChefRes(status=res['status'],  path=res['path'])