import mongoengine as db

class Categori(db.Document):
	categori 	= db.StringField()
	slug		= db.StringField()

	meta		= {
		'indexes': [
			'slug'
		]
	}