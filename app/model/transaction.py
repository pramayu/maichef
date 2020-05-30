import os
from uuid import uuid4
import mongoengine as db
from app.model.foodorder import Foodorder
from app.model.user import User
import midtransclient



class ActionsTrans(db.EmbeddedDocument):
	strid 				= db.StringField()
	name				= db.StringField()
	method				= db.StringField()
	url 				= db.StringField()

	meta 				= {
		'indexes': [
			'strid'
		]
	}

class Transaction(db.Document):
	transaction_id		= db.StringField()
	payment_type		= db.StringField()
	transaction_time	= db.DateTimeField()
	settlements_time	= db.DateTimeField()
	transaction_status	= db.StringField()
	user 				= db.ReferenceField(User, dbref=True)
	order				= db.ReferenceField(Foodorder, dbref=True)
	signature_key		= db.StringField()
	action_trans		= db.ListField(db.EmbeddedDocumentField(ActionsTrans))
	canceled_time		= db.DateTimeField()

	meta 				= {
		'indexes': [
			'transaction_id',
			'payment_type',
			'transaction_status',
			'transaction_time',
			'user',
			'order'
		]
	}


class SetupTransaction():
	def __init__(self, user_id=None):
		self.user_id	= user_id

	def find_order_id(self, order_id):
		if self.user_id:
			try:
				order = Foodorder.objects(id=order_id).only(*['id','uniqcode','total_mount','user']).first()
				return order
			except Exception as e:
				return False

	def fetch_gopay_charge(self, uniqcode, amount, email):
		if self.user_id:
			core = midtransclient.CoreApi(
    			is_production=False,
    			server_key=os.getenv('MIDTRANS_SERVER_KEY'),
    			client_key=os.getenv('MIDTRANS_SERVER_KEY')
			)
			req_payment = {
				"payment_type": "gopay",
				"transaction_details": {
					"gross_amount": amount,
					"order_id": uniqcode
				},
				"customer_details": {
					"email": email
				}
			}
			try:
				charge_response = core.charge(req_payment)
				return charge_response
			except Exception as e:
				return False

	def push_transaction_actions(self, response):
		if self.user_id:
			temp = response['actions']
			actiontrans = []
			try:
				for i in temp:
					action = ActionsTrans(strid=uuid4().hex, name=i['name'], method=i['method'], url=i['url'])
					actiontrans.append(action)
				return actiontrans
			except Exception as e:
				return False

	def insert_transaction(self, attr, order_id, actiontrans):
		if self.user_id:
			try:
				trans = Transaction(transaction_id=attr['tran_id'],payment_type=attr['pay_type'],
						transaction_time=attr['tran_time'], transaction_status=attr['tran_status'],
						user=self.user_id, order=order_id, action_trans=actiontrans)
				return trans
			except Exception as e:
				return False

	def request_transaction(self, order_id):
		res = {'status': False, 'path': 'transaction'}
		if self.user_id:
			order = self.find_order_id(order_id)
			if order:
				response = self.fetch_gopay_charge(order['uniqcode'], order['total_mount'], order['user']['email'])
				if response:
					attr = {
						'tran_id' 		: response['transaction_id'],
						'tran_status'	: response['transaction_status'],
						'pay_type'		: response['payment_type'],
						'tran_time'		: response['transaction_time']
					}
					try:
						actiontrans = self.push_transaction_actions(response)
						if actiontrans:
							transaction = self.insert_transaction(attr, order_id, actiontrans)
							transaction.save()
							res = {'status': True, 'path': 'transaction'}
							return res
					except Exception as e:
						return res
				else:
					return res
			else:
				return res
		else:
			return res

	def send_email_user(self):
		pass

	def udpate_chef_schedule(self):
		pass

	def update_transaction(self):
		pass

	def cancel_transaction(self):
		pass

	def cancel_another_order(self):
		# cancel another order with same req schedule
		pass