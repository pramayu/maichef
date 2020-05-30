from datetime import datetime

def chk_datime(datime):
	date_format = '%Y-%m-%d'
	try:
		rs = datetime.strptime(datime, date_format)
		return rs
	except ValueError:
		return False