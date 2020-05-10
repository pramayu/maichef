import mongoengine as db

class Categori(db.Document):
	categori 	= db.StringField()
	slug		= db.StringField()

	meta		= {
		'indexes': [
			'slug'
		]
	}


class SetupCategori():
	def __init__(self, categori, user_id=None, employe_id=None):
		self.categori 	= categori
		self.user_id	= user_id
		self.employe_id	= employe_id

	def slug_categori(self):
		slug = self.categori.lower().replace(" ", "_")
		return slug

	def insert_categori(self):
		res = { 'status': False, 'path': 'categori' }
		if self.user_id and self.employe_id:
			if self.categori:
				slug = self.slug_categori()
				try:
					categori = Categori(categori=self.categori, slug=slug)
					categori.save()
					res = { 'status': True, 'path': 'categori' }
					return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res

	def delete_categori(self, categori_id):
		res = { 'status': False, 'path': 'categori' }