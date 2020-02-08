from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_mail import *  
import random
from flask_jsonpify import jsonify
import json
import pymysql



app = Flask(__name__)
mail = Mail(app)  
api = Api(app)
CORS(app)
otp = random.randint(000000,999999)  


@app.route("/")
def hello():
	return jsonify({'text':'Hello World!'})

class Employees(Resource):
	def get(self):
		return {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]} 
class Employees_Name(Resource):
	def get(self, employee_id):
		print('Employee id:' + employee_id)
		result = {'data': {'id':1, 'name':'Balram'}}
		return jsonify(result)       


api.add_resource(Employees, '/employees')
api.add_resource(Employees_Name, '/employees/<employee_id>')



@app.route("/ap/",methods = ["GET"])
def get():
	mobile = request.args['phone']
	y = json.loads(mobile)
	return jsonify({'text':'success'})

@app.route('/userregister',methods = ["POST","GET"])  
def mufun():
	userdata = request.args['senduserdata']
	y = json.loads(userdata)
	mailid =  y["mailid"]
	fullname =  y["fullname"]
	username =  y["username"]
	password =  y["password"]
	email = y['mailid']

	mail = Mail(app)  
	app.config["MAIL_SERVER"]='smtp.gmail.com'  
	app.config["MAIL_PORT"] = 465     
	app.config["MAIL_USERNAME"] = 'senderMailId@gmail.com'  
	app.config['MAIL_PASSWORD'] = 'sendeMailPassword'  
	app.config['MAIL_USE_TLS'] = False  
	app.config['MAIL_USE_SSL'] = True  
	
	mail = Mail(app)  

	host = "localhost"
	user = "dbusername"
	password = "dbpassword"
	db = "register"
	import pymysql
	con = pymysql.Connection(host=host, user=user, password=password, database=db)
	cur = con.cursor()
	query = "select mailid from userregister"
	cur.execute(query)
	rows = cur.fetchall()
	con.commit()		
	con.close()
	for row in rows:
		if row[0]==email:
			error = "Email_Id already register"
			return jsonify({'response':'alreadyregister'})  
	else:
		try:
			msg = Message('OTP',sender = 'senderMailId@gmail.com', recipients = [email])
			msg.body = str(otp)
			mail.send(msg)
			print("OTP : --------------->>>>>",otp)
			return jsonify({'response':'success'})  
		except:
			return jsonify({'response':'notregistered'})

@app.route('/otpverification/',methods=["POST","GET"])  
def validate():
	userdata = request.args['senduserdata']
	print("->> " , userdata)
	print("-------------------------------------")
	y = json.loads(userdata)
	
	user_otp = y['otp']
	mailid =  y["mailid"]
	fullname =  y["fullname"]
	username =  y["username"]
	password =  y["password"]

	print("->> " , userdata)
	print("otp->> " , otp)
	print("user_otp->> " , user_otp)
	
	if otp == int(user_otp):
		host = "localhost"
		user = "dbusername" 
		password = "dbpassword" 
		db = "register"
		con = pymysql.Connection(host = host,user = user,password = password,database = db) 
		cur = con.cursor() 

		print("query_data--->>>", mailid, fullname, username, password)

		q="INSERT INTO userregister(mailid, fullname, username, password) values(%s, %s, %s, %s)"
		cur.execute(q,(mailid, fullname, username, password))
		con.commit()
		con.close()
		return jsonify({'response':'success'})
	else:
		return jsonify({'response':'reject'})

@app.route('/userlogin',methods = ["POST","GET"])  
def check_login(): 
	userdata = request.args['logininfo']
	print("->> " , userdata)
	print("-------------------------------------")
	y = json.loads(userdata)
	User_id = y['username']
	Password =  y["password"]

	host = "localhost"
	user = "dbusername"
	ap = "dbpassword"
	db = "register"
	con = pymysql.Connection(host=host, user=user, password=ap, database=db)
	cur = con.cursor()
	query1 = "select username from userregister"
	query2 = "select password from userregister"

	cur.execute(query1)
	rows1 = cur.fetchall()

	cur.execute(query2)
	rows2 = cur.fetchall()

	loginInfo = {}
	loginInfo = dict(zip(rows1, rows2))

	con.commit()
	con.close()
	print("logininfo-->>",loginInfo)
	for key, value in loginInfo.items():
		if key[0] == User_Id and value[0] == Password:
			return jsonify({'response':'success'})
	else:	
		return jsonify({'response':'reject'})
	return jsonify({'response':'reject'})
  

if __name__ == '__main__':
	app.run(port=5000, debug = True)
