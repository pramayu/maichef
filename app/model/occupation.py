import mongoengine as db


class Occupation(db.Document):
	role		= db.StringField()
	slug		= db.StringField()

	meta		= {
		'indexes': [
			'slug'
		]
	}

class SetupOccupation():
	def __init__(self, occupation):
		self.occupation = occupation

	def slug(self):
		if len(self.occupation) != 0:
			slug = self.occupation.lower().replace(" ","_")
			return slug
		else:
			return False

	def insert_occupation(self):
		res = {'status': False, 'path': 'occupation'}
		if len(self.occupation) != 0:
			slug = self.slug()
			try:
				occz = Occupation.objects(slug=slug).first()
				if occz:
					return res
				else:
					occu = Occupation(role=self.occupation, slug=slug)
					occu.save()
					res = {'status': True, 'path': 'occupation'}
					return res
			except Exception as e:
				return res
			return res
		else:
			return res

	def update_occupation(self, slug):
		res = {'status': False, 'path': 'occupation'}
		if len(self.occupation) and len(slug) != 0:
			nslug = self.slug()
			try:
				occu = Occupation.objects(slug=slug).first()
				if occu:
					occu['role'] = self.occupation
					occu['slug'] = nslug
					occu.save()
					res = {'status': True, 'path': 'occupation'}
					return res
				else:
					return res
			except Exception as e:
				return res
		else:
			return res