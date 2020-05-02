import jwt
from os import path
from flask import request
from functools import wraps
from app.common.middleware.buildtoken import checktoken


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
							acc_token = checktoken(x_accesse_token)
							if acc_token['id'] == kwargs['userid']:
								current_user = {
									'isAuth'	: True,
									'id'		: acc_token['id'],
									'username'	: acc_token['username']
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