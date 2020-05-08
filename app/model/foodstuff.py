import mongoengine as db
from app.model.chef import Chef
from app.model.kitchentool import Kitchentool
from app.model.categori import Categori



class Ingredient(db.EmbeddedDocument):
	strid 		= db.StringField()
	ingredient	= db.StringField()
	number		= db.StringField()

	meta 		= {
		'indexes': [
			'strid'
		]
	}

class Foodstuff(db.Document):
	title		= db.StringField()
	slug		= db.StringField()
	price		= db.FloatField()
	descrip		= db.StringField()
	status		= db.StringField(default="pending") #pending, draf, approve
	servtime	= db.StringField()
	servstatus	= db.BooleanField(default=True)
	categories	= db.ListField(db.ReferenceField(Categori, dbref=True))
	ingredients	= db.ListField(db.EmbeddedDocumentField(Ingredient))
	owner		= db.ReferenceField(Chef, dbref=True)
	kitchentool = db.ListField(db.ReferenceField(Kitchentool, dbref=True))

	meta		= {
		'indexes': [
			'slug',
			'status',
			'servtime',
			'categories'
		]
	}


class SetupFoodstuff():
	def __init__(self, user_id=None, chef_id=None, str_id=None, foodstuff_id=None):
		self.str_id			= str_id
		self.user_id		= user_id
		self.chef_id		= chef_id
		self.foodstuff_id	= foodstuff_id

	def create_slug(self, title):
		pass

	def insert_foodstuff(self, attribute):
		pass

	def update_foodstuff(self, attribute):
		pass

	def push_ingredient(self, ingredient):
		pass

	def pull_ingredient(self):
		pass