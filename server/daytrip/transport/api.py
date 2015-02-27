import facebook
from flask import request
from flask_restful import Resource, reqparse
import db


#ALL QUERIES MUST BE AUTHENTICATED WITH AN AUTHENTICATION TOKEN (Except for the AUTH POST)

#Add the token as part of a query string, and check db.sqlite.check_authorization(token)



class Test(Resource):
	def get(self):
		return {"message": "HelloWorld"}, 200  #Return a python object and a status code!


class Test2(Resource):
	def post(self, parameter):
		json_data = request.get_json(force=True)
		return {"received": json_data, "parameter": parameter}, 200 #Return the posted data with a status code


class Auth(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('token', type=str, required = True, help="No token to verify", location='json')
		self.reqparse.add_argument('user_id', type=str, required = True, help="An associated Facebook User ID is required", location='json')
		super(Auth, self).__init__()

	def post(self):
		args = self.reqparse.parse_args()
		token = args['token']
		uid = args['user_id']

		graph = facebook.GraphAPI(access_token=token)
		user = graph.get_object(id=uid)
		if(user and user['id']==uid):

			#add token to repository if not exists
			if not db.sqlite.check_authorization(token):
				db.sqlite.add_authorization(token, uid)

			#add to user repository if not exists
			if not db.sqlite.user_exists(uid):
				db.sqlite.create_user(uid, user['first_name'], user['last_name'], user['email'])

			return True, 200;

class Itinerary(Resource):

	def get(self, id):
		pass

	def put(self, id):
		pass

	def delete(self, id):
		pass

class Create_Itinerary(Resource):

	def post(self):
		pass


class Item(Resource):
	def get(self, id):
		pass

	def put(self, id):
		pass

	def delete(self, id):
		pass
