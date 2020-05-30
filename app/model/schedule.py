import mongoengine as db
from datetime import datetime
from app.model.chef import Chef


class Workdetail(db.EmbeddedDocument):
	strid 			= db.StringField()
	time 			= db.StringField() #'%H:%M:%S'
	build 			= db.StringField(default=datetime.now)
	updated 		= db.StringField()
	status			= db.StringField(default='ongoing') #ongoing, completed, canceled
	# order 			= db.ReferenceField(Order, dbref=True)

	meta 			= {
		'indexes': [
			'strid'
		]
	}

class Schedulechef(db.Document):
	datime 			= db.DateTimeField()
	workdetail 		= db.ListField(db.EmbeddedDocumentField(Workdetail))
	status 			= db.BooleanField(default=True) #true = on / false = off
	chef 			= db.ReferenceField(Chef, dbref=True)
	build 			= db.DateTimeField(default=datetime.now)

	meta 			= {
		'indexes': [
			'datime',
			'status',
			'chef'
		]
	}

class SetupChefSchedule():
	def __init__(self, user_id=None, chef_id=None, str_id=None, schedule_id=None,):
		self.user_id		= user_id
		self.chef_id 		= chef_id
		self.str_id			= str_id
		self.schedule_id	= schedule_id

	def find_schedule_datime(self, datime):
		if self.user_id:
			schedule = Schedulechef.objects(datime=datime).first()
			return schedule

	def check_schedule(self, datime):
		pass
		# find schedule by chef id for this mount

	def modif_chef_schedule(self, datime):
		res = {'status': False, 'path': 'push_chef_schedule'}
		if self.user_id and self.chef_id:
			if datime:
				schedule = self.find_schedule_datime(datime)
				if schedule:
					# update
					if self.chef_id == schedule['chef']['id']:
						schedule['status'] = not schedule['status']
						schedule.save()
						res = {'status': True, 'path': 'push_chef_schedule'}
						return res
					else:
						return res
				else:
					# create
					store = Schedulechef(datime=datime, chef=self.chef_id, status=False)
					store.save()
					res = {'status': True, 'path': 'push_chef_schedule'}
					return res
			else:
				return res
		else:
			return res

	def push_order_schedule(self, datime, order_id):
		pass
