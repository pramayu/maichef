import re

def chk_input(title,price):
	regex		= '[@!#$%^&*()<>?/\|}{~:]'
	isPrice		= price.isdigit()
	isTitle		= re.search(regex, title)

	if isPrice == True and isTitle == None:
		return True