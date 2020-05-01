class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConf(Config):
	DEBUG = True
	TESTING = True
	MONGODB_DB = 'maichefs'
	MONGODB_HOST = '127.0.0.1'
	MONGODB_PORT = 27017

class ProductionConf(Config):
	pass