import bcrypt
import mongoengine as db
from random import randrange
from datetime import datetime
from mongoengine.queryset.visitor import Q
from app.common.chk_input.user import signup_chk




class User(db.Document):
	username		= db.StringField()
	hashtext		= db.StringField()
	email			= db.EmailField()
	uniquepin		= db.StringField()
	build			= db.DateTimeField(default=datetime.utcnow)
	activeuser		= db.BooleanField(default=False)
	

	meta			= {
		'indexes': [
			'username',
			'email',
			'uniquepin'
		]
	}

class Useraddress(db.Document):
	street 			= db.StringField()
	regenci			= db.StringField()
	province 		= db.StringField()
	point 			= db.GeoPointField()
	choosed			= db.BooleanField(default=True)
	user 			= db.ReferenceField(User, dbref=True)

	meta 			= {
		'indexes': [
			'regenci',
			'province',
			'point'
		]
	}


class SetupUser():
	def __init__(self):
		pass

	def insertuser(self, username, hashtext, email):
		res = { 'status': False, 'path': 'createuser' }
		reqfields = ['id','username']
		chkinput = signup_chk(username, email)
		user = User.objects(Q(username=username) or Q(email=email)).only(*reqfields).first()
		if user:
			return res
		else:
			if len(hashtext) != 0 and chkinput == True:
				hashtext = bcrypt.hashpw(hashtext, bcrypt.gensalt(12))
				try:
					user = User(username=username, hashtext=hashtext,
								email=email, uniquepin=str(randrange(1, 9999, 4)))
					user.save()
					res = { 'status': True, 'path': 'createuser' }
					return res
				except Exception as e:
					return res
			else:
				return res

	def useractive(self, uniqpin):
		res = { 'status': False, 'path': 'activeuser' }
		reqfields = ['id','username', 'uniquepin', 'activeuser']
		if len(uniqpin) != 0:
			user = User.objects(Q(uniquepin=uniqpin) and Q(activeuser=False)).only(*reqfields).first()
			if user:
				try:
					user['activeuser'] = True
					store = user.save()
					res = { 'status': True, 'path': 'activeuser', 'user': store }
					return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res

	def checkusertoken(self, userid):
		res = { 'status': False, 'path': 'checkusertoken' }
		reqfields = ['id','username']
		if len(userid) != 0:
			try:
				user = User.objects(id=userid).only(*reqfields).first()
				if user:
					res = {
						'user'		: user, 
						'status'	: False,
						'path'		: 'checkusertoken',
					}
					return res
				else:
					return res
			except Exception as e:
				return res
		else:
			return res

	def identityuser(self, identity, password):
		res = { 'status': False, 'path': 'identityuser' }
		if len(identity) and len(password) != 0:
			reqfields = ['id','username','email','hashtext']
			user = User.objects(Q(username=identity) or Q(email=identity)).only(*reqfields).first()
			if user:
				match = bcrypt.checkpw(password, user['hashtext'].encode('utf-8'))
				if match:
					res = { 'status': True, 'path': 'identityuser', 'user': user }
					return res
				else:
					return res
			else:
				return res
		else:
			return res


class SetupUserAttribute():

	def __init__(self, user_id=None, addr_id=None):
		self.user_id 	= user_id
		self.addr_id 	= addr_id

	def find_user_addr_id(self):
		if self.user_id:
			addr = Useraddress.objects(id=self.addr_id).first()
			return addr

	def find_user_addrs(self):
		if self.user_id:
			addrs = Useraddress.objects(user=self.user_id)
			return addrs

	def find_index_addr(self, addrs):
		if self.user_id:
			indx = next((indx for (indx, i) in enumerate(addrs) if self.addr_id == i['id']), None)
			return indx

	def find_index_true_addr(self, addrs):
		if self.user_id:
			indx = next((indx for (indx, i) in enumerate(addrs) if i['choosed'] == True), None)
			return indx

	def create_user_address(self, stre, rege, prov, poin):
		if self.user_id:
			addr = Useraddress(street=stre,regenci=rege,province=prov,point=poin,user=self.user_id)
			save = addr.save()
			return save

	def update_choose_address(self, addrs, indx):
		if self.user_id:
			try:
				Useraddress.objects(id=addrs[indx]['id']).update(choosed=not addrs[indx]['choosed'])
				return True
			except Exception as e:
				return False
			

	def push_user_address(self, attr):
		res = {'status': False, 'path': 'push_user_address'}
		if self.user_id:
			if len(attr) != 0:
				stre 		= attr['street']
				rege		= attr['regenci']
				prov		= attr['province']
				poin 		= attr['point']
				try:
					addrs = self.find_user_addrs()
					if addrs:
						addr = self.create_user_address(stre, rege, prov, poin)
						if addr:
							indx = self.find_index_true_addr(addrs)
							Useraddress.objects(id=addrs[indx]['id']).update_one(choosed=False)
						addr.save()
						res = {'status': True, 'path': 'push_user_address'}
						return res
					else:
						addr = self.create_user_address(stre, rege, prov, poin)
						if addr:
							res = {'status': True, 'path': 'push_user_address'}
							return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res

	def update_user_address(self, attr):
		res = {'status': False, 'path': 'update_user_address'}
		if self.user_id and self.addr_id:
			if len(attr) != 0:
				addr = self.find_user_addr_id()
				if addr and addr['user']['id'] == self.user_id:
					try:
						stre 		= attr['street']
						rege		= attr['regenci']
						prov		= attr['province']
						poin 		= attr['point']

						addr['province'] 	= prov if addr['province'] != prov else addr['province']
						addr['regenci']		= rege if addr['regenci'] != rege else addr['regenci']
						addr['street'] 		= stre if addr['street'] != stre else addr['street']
						addr['point'] 		= poin
						addr.save()

						res = {'status': True, 'path': 'update_user_address'}
						return res

					except Exception as e:
						return res
				else:
					return res
			else:
				return res
		else:
			return res

	def pull_user_address(self):
		res = {'status': False, 'path': 'pull_user_address'}
		if self.user_id and self.addr_id:
			addr = self.find_user_addr_id()
			if addr:
				try:
					addr.delete()
					res = {'status': True, 'path': 'pull_user_address'}
					return res
				except Exception as e:
					return res
			else:
				return res
		else:
			return res

	def choose_user_address(self):
		res = {'status': False, 'path': 'choose_user_address'}
		if self.user_id and self.addr_id:
			addrs = self.find_user_addrs()
			if addrs:
				if any(self.addr_id == addr['id'] for addr in addrs):
					if any(addr['choosed'] == True for addr in addrs):
						indx = self.find_index_true_addr(addrs)
						self.update_choose_address(addrs, indx)
					indx = self.find_index_addr(addrs)
					update = self.update_choose_address(addrs, indx)
					if update:
						res = {'status': True, 'path': 'pull_user_address'}
						return res
					else:
						return res
				else:
					return res
			else:
				return res
		else:
			return res
