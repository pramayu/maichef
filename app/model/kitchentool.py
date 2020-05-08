import mongoengine as db


class Kitchentool(db.Document):
	stuff		= db.StringField()
	slug		= db.StringField()

	meta 		= {
		'indexes': [
			'slug'
		]
	}