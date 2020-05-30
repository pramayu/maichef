import graphene as grap
from app.api.service.transaction.transaction_api import RequestPaymentCharge


class TranServ(grap.ObjectType):
	requestpaymentcharge		= RequestPaymentCharge.Field()