import re


def signup_chk(username, email):
		regex_username = '[@!#$%^&*()<>?/\|}{~:]'
		regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
		chkusername = re.search(regex_username, username)
		chkemail = re.search(regex_email, email)
		if len(username) and len(email) != 0:
			if ' ' not in username and ' ' not in email:
				if chkusername == None and chkemail != None:
					return True