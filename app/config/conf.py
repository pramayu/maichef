class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConf(Config):
	DEBUG = True
	TESTING = True

class ProductionConf(Config):
	pass