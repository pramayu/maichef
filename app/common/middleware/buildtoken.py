import jwt
from os import path

def buildtoken(payload):
	private = open(path.join('app/common/assets/jwtRS256.key'), 'r').read()
	token = jwt.encode(payload, private, algorithm='RS256').decode('utf-8')
	return token


def checktoken(token):
	public = open(path.join('app/common/assets/jwtRS256.key.pub'), 'r').read()
	payload = jwt.decode(token, public, algorithms='RS256')
	return payload