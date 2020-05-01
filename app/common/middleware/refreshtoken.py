import jwt
from os import path

def buildrefresh(payload):
	private = open(path.join('app/common/assets/jwtRS256.key'), 'r').read()
	refreshtoken = jwt.encode(payload, private, algorithm='RS256').decode('utf-8')
	return refreshtoken


def checkrefresh(token):
	public = open(path.join('app/common/assets/jwtRS256.key.pub'), 'r').read()
	refreshtoken = jwt.decode(token, public, algorithms='RS256')
	return refreshtoken