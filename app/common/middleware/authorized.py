import jwt
from os import path
from flask import request
from functools import wraps
from app.model.user import User as UserModel
from app.model.chef import Chef as ChefModel
from app.common.middleware.buildtoken import checktoken
from app.common.middleware.JSONDecoder import JSONDecoder


def requireauth(fn):
	@wraps(fn)

	def decoration(*args, **kwargs):
		current_user	= { 'isAuth':False }
		if 'x-refresh-token' in request.headers and 'x-accesse-token' in request.headers:
			x_refresh_token = request.headers['x-refresh-token']
			x_accesse_token = request.headers['x-accesse-token']
			if x_refresh_token != x_accesse_token:
				try:
					ref_token = checktoken(x_refresh_token)
					if ref_token:
						try:
							user_id = JSONDecoder(kwargs['userid'])
							user = UserModel.objects(id=user_id).only(*['id','username']).first()
															
							acc_token 	= checktoken(x_accesse_token)
							acc_user_id	= JSONDecoder(acc_token['id'])

							if user['id'] == acc_user_id:
								current_user = {
									'isAuth'	: True,
									'user_id'	: user['id'],
									'username'	: user['username']
								}
							else:
								current_user
						except (KeyError, jwt.ExpiredSignatureError, jwt.DecodeError):
							current_user
					else:
						current_user
				except (KeyError, jwt.ExpiredSignatureError, jwt.DecodeError):
					current_user
			else:
				current_user
		else:
			current_user
		return fn(current_user, *args, **kwargs)
	return decoration