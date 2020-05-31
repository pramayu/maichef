from app import app

if '__main__' == __name__:
	# app.run(host="192.168.1.9", port="5000")
	app.run(host='0.0.0.0',port=8000)