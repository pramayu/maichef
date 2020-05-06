import mongoengine as db
from app.model.chef import Chef


class Schedule(db.Document):
	date		= db.DateTimeField()
	chef 		= db.ReferenceField(Chef, dbref=True)
	status		= db.StringField(default="less") #less, full, completed, offday 
	# paid order

	meta		= {
		'indexes': [
			'date'
		]
	}