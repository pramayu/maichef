import os
class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConf(Config):
	DEBUG = True
	TESTING = True
	# MONGODB_DB = 'db_maichefs'
	# MONGODB_HOST = '127.0.0.1'
	# MONGODB_PORT = 27017
	# MONGODB_DB='db_maichefs'
	# MONGODB_PASSWORD='maichefs'
	# MONGODB_USERNAME='maichefs'
	# MONGODB_HOST="mongodb+srv://maichefs:maichefs@cluster0-mplbr.gcp.mongodb.net/db_maichefs?retryWrites=true&w=majority"
	# MONGODB_HOST=os.getenv('MONGODB_URI')

class ProductionConf(Config):
	pass